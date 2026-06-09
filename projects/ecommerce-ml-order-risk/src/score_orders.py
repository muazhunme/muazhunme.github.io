import warnings

import pandas as pd
import joblib

from config import (
    CV_BEST_MODEL_PATH,
    HIGH_RISK_ORDERS_SAMPLE,
    MODEL_DATASET,
    REPORTS_DIR,
    SCORED_ORDERS,
)
from modeling_utils import make_feature_matrix, predict_scores


warnings.filterwarnings("ignore", message="X does not have valid feature names.*")
warnings.filterwarnings("ignore", category=UserWarning, module="joblib.*")

def risk_band(score: float) -> str:
    if score >= 0.80:
        return "critical"
    if score >= 0.60:
        return "high"
    if score >= 0.30:
        return "medium"
    return "low"


def recommended_action(score: float) -> str:
    band = risk_band(score)
    if band == "critical":
        return "Immediate support review and proactive customer follow-up"
    if band == "high":
        return "Prioritize for support monitoring"
    if band == "medium":
        return "Monitor order and seller/category signals"
    return "No immediate action"


def top_risk_reasons(row: pd.Series) -> str:
    reasons = []

    if row.get("delivery_delay_days", 0) > 0:
        reasons.append(f"delivery delayed by {row['delivery_delay_days']:.1f} days")
    if row.get("is_late", 0) == 1 and "delivery delayed" not in " ".join(reasons):
        reasons.append("order delivered after estimated date")
    if row.get("seller_prior_bad_review_rate", 0) >= 0.20:
        reasons.append("seller has elevated prior bad-review rate")
    if row.get("category_prior_bad_review_rate", 0) >= 0.18:
        reasons.append("category has elevated prior bad-review rate")
    if row.get("seller_prior_late_rate", 0) >= 0.15:
        reasons.append("seller has elevated prior late-delivery rate")
    if row.get("order_item_count", 0) >= 3:
        reasons.append("multi-item order increases operational complexity")
    if row.get("freight_ratio", 0) >= 0.50:
        reasons.append("freight cost is high relative to item price")
    if row.get("delivery_time_days", 0) >= 25:
        reasons.append("long delivery time")

    if not reasons:
        reasons.append("model score driven by combined order, seller, category, and payment signals")
    return "; ".join(reasons[:3])


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(MODEL_DATASET)
    X = make_feature_matrix(data)
    model = joblib.load(CV_BEST_MODEL_PATH)
    scores = predict_scores(model, X)

    output_columns = [
        "order_id",
        "bad_review",
        "review_score",
        "order_status",
        "product_category",
        "seller_state",
        "customer_state",
        "delivery_time_days",
        "delivery_delay_days",
        "seller_prior_bad_review_rate",
        "category_prior_bad_review_rate",
    ]
    scored = data[[column for column in output_columns if column in data.columns]].copy()
    scored["risk_score"] = scores
    scored["risk_band"] = scored["risk_score"].map(risk_band)
    scored["top_risk_reason"] = data.apply(top_risk_reasons, axis=1)
    scored["recommended_action"] = scored["risk_score"].map(recommended_action)
    scored = scored.sort_values("risk_score", ascending=False)

    scored.to_csv(SCORED_ORDERS, index=False)
    scored.head(100).to_csv(HIGH_RISK_ORDERS_SAMPLE, index=False)

    print(f"Saved scored orders to {SCORED_ORDERS}")
    print(f"Saved top-risk sample to {HIGH_RISK_ORDERS_SAMPLE}")


if __name__ == "__main__":
    main()
