import warnings

import pandas as pd
import joblib
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from config import (
    BUSINESS_THRESHOLD_RESULTS,
    BUSINESS_THRESHOLD_SUMMARY,
    CV_BEST_MODEL_PATH,
    MODEL_DATASET,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET_COLUMN,
)
from modeling_utils import predict_scores, split_features_target


warnings.filterwarnings("ignore", message="X does not have valid feature names.*")
warnings.filterwarnings("ignore", category=UserWarning, module="joblib.*")

MISSED_BAD_REVIEW_COST = 100
UNNECESSARY_INTERVENTION_COST = 10
SUCCESSFUL_INTERVENTION_SAVINGS = 60


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(MODEL_DATASET)
    X, y = split_features_target(data)
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    model = joblib.load(CV_BEST_MODEL_PATH)
    scores = predict_scores(model, X_test)
    no_model_cost = int(y_test.sum()) * MISSED_BAD_REVIEW_COST

    rows = []
    for threshold in [round(value / 100, 2) for value in range(10, 91, 5)]:
        predictions = (scores >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
        total_cost = (
            fn * MISSED_BAD_REVIEW_COST
            + fp * UNNECESSARY_INTERVENTION_COST
            + tp * (MISSED_BAD_REVIEW_COST - SUCCESSFUL_INTERVENTION_SAVINGS)
        )
        cost_savings = no_model_cost - total_cost
        rows.append(
            {
                "threshold": threshold,
                "flagged_orders": int(tp + fp),
                "flagged_order_rate": float((tp + fp) / len(y_test)),
                "true_positives": int(tp),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_negatives": int(tn),
                "precision": float(tp / (tp + fp)) if (tp + fp) else 0.0,
                "recall": float(tp / (tp + fn)) if (tp + fn) else 0.0,
                "estimated_cost": float(total_cost),
                "estimated_savings_vs_no_model": float(cost_savings),
            }
        )

    results = pd.DataFrame(rows)
    results.to_csv(BUSINESS_THRESHOLD_RESULTS, index=False)

    best = results.sort_values("estimated_savings_vs_no_model", ascending=False).iloc[0]
    summary = f"""# Business Threshold Summary

## Cost Assumptions

These are simple placeholder assumptions used to make threshold selection business-oriented:

```text
Missed bad review cost:              {MISSED_BAD_REVIEW_COST}
Unnecessary support intervention:    {UNNECESSARY_INTERVENTION_COST}
Successful intervention savings:     {SUCCESSFUL_INTERVENTION_SAVINGS}
```

The purpose is not to claim exact financial value. The purpose is to show how a company would connect model thresholds to operational cost.

## Recommended Threshold

```text
Threshold:                    {best["threshold"]:.2f}
Flagged order rate:            {best["flagged_order_rate"]:.2%}
Precision:                     {best["precision"]:.4f}
Recall:                        {best["recall"]:.4f}
Estimated savings vs no model: {best["estimated_savings_vs_no_model"]:.0f}
```

## Interpretation

This threshold is the best option under the current cost assumptions. If support capacity is limited, the business may choose a higher threshold to review fewer orders with higher precision. If customer retention is the priority, the business may choose a lower threshold to catch more risky orders.

Full threshold table:

```text
reports/business_threshold_analysis.csv
```
"""
    BUSINESS_THRESHOLD_SUMMARY.write_text(summary, encoding="utf-8")
    print(f"Saved business threshold analysis to {BUSINESS_THRESHOLD_RESULTS}")
    print(f"Saved business threshold summary to {BUSINESS_THRESHOLD_SUMMARY}")


if __name__ == "__main__":
    main()
