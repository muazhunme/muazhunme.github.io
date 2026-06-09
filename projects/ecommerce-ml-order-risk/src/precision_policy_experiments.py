import json
import warnings

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import average_precision_score, confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from config import (
    CRITICAL_RISK_MODEL_PATH,
    CV_TUNING_RESULTS,
    MODEL_DATASET,
    PRECISION_FOCUSED_MODEL_PATH,
    PRECISION_POLICY_RESULTS,
    PRECISION_POLICY_SUMMARY,
    RANDOM_STATE,
    REPORTS_DIR,
)
from modeling_utils import build_preprocessor, predict_scores, split_features_target


warnings.filterwarnings("ignore", message="X does not have valid feature names.*")
warnings.filterwarnings("ignore", category=UserWarning, module="joblib.*")

MIN_RECALL_TARGETS = [0.25, 0.35, 0.45, 0.55]
TOP_K_RATES = [0.05, 0.10, 0.15]


def load_best_lightgbm_params() -> dict:
    results = pd.read_csv(CV_TUNING_RESULTS)
    final_row = results[results["trial"].astype(str) == "final_test"].iloc[0]
    return json.loads(final_row["params"])


def make_pipeline(X_train: pd.DataFrame, params: dict, class_weight):
    params = {**params, "n_jobs": -1}
    model = LGBMClassifier(
        **params,
        class_weight=class_weight,
        random_state=RANDOM_STATE,
        verbose=-1,
    )
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(X_train)),
            ("model", model),
        ]
    )


def metrics_at_threshold(y_true, scores, threshold: float) -> dict:
    predictions = (scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, predictions).ravel()
    return {
        "threshold": float(threshold),
        "flagged_orders": int(tp + fp),
        "flagged_order_rate": float((tp + fp) / len(y_true)),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_negatives": int(tn),
    }


def best_threshold_for_min_recall(y_valid, valid_scores, min_recall: float) -> tuple[float, dict]:
    grid_thresholds = np.linspace(0.05, 0.95, 181)
    score_quantiles = pd.Series(valid_scores).quantile(np.linspace(0.50, 0.99, 100)).to_numpy()
    candidate_thresholds = sorted(set(np.concatenate([grid_thresholds, score_quantiles]).round(5)), reverse=True)
    best_threshold = 0.5
    best_metrics = None

    for threshold in candidate_thresholds:
        metrics = metrics_at_threshold(y_valid, valid_scores, threshold)
        if metrics["recall"] < min_recall:
            continue
        if best_metrics is None:
            best_threshold = threshold
            best_metrics = metrics
            continue

        is_better_precision = metrics["precision"] > best_metrics["precision"]
        same_precision_higher_threshold = (
            metrics["precision"] == best_metrics["precision"]
            and metrics["threshold"] > best_metrics["threshold"]
        )
        if is_better_precision or same_precision_higher_threshold:
            best_threshold = threshold
            best_metrics = metrics

    if best_metrics is None:
        best_threshold = float(pd.Series(valid_scores).quantile(0.95))
        best_metrics = metrics_at_threshold(y_valid, valid_scores, best_threshold)

    return float(best_threshold), best_metrics


def threshold_for_top_k(valid_scores, top_k_rate: float) -> float:
    return float(pd.Series(valid_scores).quantile(1 - top_k_rate))


def add_policy_rows(rows, model_name, target_name, y_valid, valid_scores, y_test, test_scores) -> None:
    for min_recall in MIN_RECALL_TARGETS:
        threshold, valid_metrics = best_threshold_for_min_recall(y_valid, valid_scores, min_recall)
        test_metrics = metrics_at_threshold(y_test, test_scores, threshold)
        rows.append(
            {
                "model": model_name,
                "target": target_name,
                "policy": f"max_precision_with_validation_recall_at_least_{min_recall:.2f}",
                "selection_metric": "precision subject to minimum validation recall",
                **{f"validation_{key}": value for key, value in valid_metrics.items()},
                **{f"test_{key}": value for key, value in test_metrics.items()},
            }
        )

    for top_k_rate in TOP_K_RATES:
        threshold = threshold_for_top_k(valid_scores, top_k_rate)
        valid_metrics = metrics_at_threshold(y_valid, valid_scores, threshold)
        test_metrics = metrics_at_threshold(y_test, test_scores, threshold)
        rows.append(
            {
                "model": model_name,
                "target": target_name,
                "policy": f"review_top_{int(top_k_rate * 100)}pct_highest_risk_orders",
                "selection_metric": "fixed support capacity",
                **{f"validation_{key}": value for key, value in valid_metrics.items()},
                **{f"test_{key}": value for key, value in test_metrics.items()},
            }
        )


def make_summary(results: pd.DataFrame) -> str:
    bad_review_results = results[results["target"] == "bad_review"].copy()
    high_precision = bad_review_results.sort_values(
        ["test_precision", "test_recall"],
        ascending=[False, False],
    ).head(5)

    balanced_candidates = bad_review_results[bad_review_results["test_recall"] >= 0.35].copy()
    balanced = balanced_candidates.sort_values(
        ["test_precision", "test_recall"],
        ascending=[False, False],
    ).head(5)

    critical_results = results[results["target"] == "critical_one_star_review"].copy()
    critical_best = critical_results.sort_values(
        ["test_precision", "test_recall"],
        ascending=[False, False],
    ).head(3)

    return f"""# Precision Policy Summary

## Purpose

This experiment tested ways to increase precision without replacing the champion model blindly.

Safeguards used:

- thresholds were selected on validation data
- final results were measured on held-out test data
- the original champion model remains unchanged
- precision-focused and critical-risk models are treated as challenger policies

## Best High-Precision Bad-Review Policies

{high_precision[["model", "policy", "test_threshold", "test_flagged_order_rate", "test_precision", "test_recall", "test_true_positives", "test_false_positives"]].to_string(index=False)}

## Best Bad-Review Policies With At Least 35% Test Recall

{balanced[["model", "policy", "test_threshold", "test_flagged_order_rate", "test_precision", "test_recall", "test_true_positives", "test_false_positives"]].to_string(index=False)}

## Critical One-Star Risk Model

{critical_best[["model", "policy", "test_threshold", "test_flagged_order_rate", "test_precision", "test_recall", "test_true_positives", "test_false_positives"]].to_string(index=False)}

## Interpretation

Precision can be increased by using stricter thresholds or top-k review policies. This reduces false positives and support workload, but it also lowers recall, meaning more bad-review orders are missed.

The production-style recommendation is to keep the CV-tuned LightGBM model as the champion ranking model and expose multiple operating modes:

```text
Balanced mode: use the existing 0.50 threshold.
High-precision mode: review only the top 5-10% highest-risk orders.
Critical-risk mode: use the separate one-star model for severe cases.
```

Full results:

```text
reports/precision_policy_results.csv
```
"""


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(MODEL_DATASET)
    X, y_bad_review = split_features_target(data)
    y_critical = (data["review_score"] <= 1).astype(int)
    params = load_best_lightgbm_params()

    X_train_valid, X_test, y_bad_train_valid, y_bad_test, y_critical_train_valid, y_critical_test = train_test_split(
        X,
        y_bad_review,
        y_critical,
        test_size=0.2,
        stratify=y_bad_review,
        random_state=RANDOM_STATE,
    )
    X_train, X_valid, y_bad_train, y_bad_valid, y_critical_train, y_critical_valid = train_test_split(
        X_train_valid,
        y_bad_train_valid,
        y_critical_train_valid,
        test_size=0.25,
        stratify=y_bad_train_valid,
        random_state=RANDOM_STATE,
    )

    model_specs = [
        ("champion_balanced_lightgbm", y_bad_train, y_bad_valid, y_bad_test, "bad_review", "balanced", None),
        ("precision_weighted_lightgbm", y_bad_train, y_bad_valid, y_bad_test, "bad_review", {0: 1, 1: 2}, PRECISION_FOCUSED_MODEL_PATH),
        ("unweighted_precision_lightgbm", y_bad_train, y_bad_valid, y_bad_test, "bad_review", None, None),
        ("critical_one_star_lightgbm", y_critical_train, y_critical_valid, y_critical_test, "critical_one_star_review", "balanced", CRITICAL_RISK_MODEL_PATH),
    ]

    rows = []
    for model_name, y_train, y_valid, y_test, target_name, class_weight, model_path in model_specs:
        pipeline = make_pipeline(X_train, params, class_weight)
        pipeline.fit(X_train, y_train)

        if model_path is not None:
            joblib.dump(pipeline, model_path)

        valid_scores = predict_scores(pipeline, X_valid)
        test_scores = predict_scores(pipeline, X_test)

        add_policy_rows(
            rows,
            model_name,
            target_name,
            y_valid,
            valid_scores,
            y_test,
            test_scores,
        )

        rows.append(
            {
                "model": model_name,
                "target": target_name,
                "policy": "ranking_quality_no_fixed_threshold",
                "selection_metric": "ranking metrics",
                "validation_threshold": None,
                "validation_flagged_orders": None,
                "validation_flagged_order_rate": None,
                "validation_precision": None,
                "validation_recall": None,
                "validation_true_positives": None,
                "validation_false_positives": None,
                "validation_false_negatives": None,
                "validation_true_negatives": None,
                "test_threshold": None,
                "test_flagged_orders": None,
                "test_flagged_order_rate": None,
                "test_precision": None,
                "test_recall": None,
                "test_true_positives": None,
                "test_false_positives": None,
                "test_false_negatives": None,
                "test_true_negatives": None,
                "validation_pr_auc": average_precision_score(y_valid, valid_scores),
                "validation_roc_auc": roc_auc_score(y_valid, valid_scores),
                "test_pr_auc": average_precision_score(y_test, test_scores),
                "test_roc_auc": roc_auc_score(y_test, test_scores),
            }
        )

    results = pd.DataFrame(rows)
    results.to_csv(PRECISION_POLICY_RESULTS, index=False)
    PRECISION_POLICY_SUMMARY.write_text(make_summary(results), encoding="utf-8")

    print(f"Saved precision policy results to {PRECISION_POLICY_RESULTS}")
    print(f"Saved precision policy summary to {PRECISION_POLICY_SUMMARY}")
    print(f"Saved precision-focused model to {PRECISION_FOCUSED_MODEL_PATH}")
    print(f"Saved critical-risk model to {CRITICAL_RISK_MODEL_PATH}")


if __name__ == "__main__":
    main()
