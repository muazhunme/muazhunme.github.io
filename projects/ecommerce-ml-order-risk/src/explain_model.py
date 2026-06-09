import joblib
import numpy as np
import pandas as pd
import shap

from config import (
    ADVANCED_BEST_MODEL_PATH,
    ERROR_ANALYSIS_DIR,
    POST_DELIVERY_DATASET,
    RANDOM_STATE,
    SHAP_IMPORTANCE_RESULTS,
)
from modeling_utils import (
    load_modeling_data,
    make_train_valid_test_split,
    predict_scores,
    predictions_at_threshold,
    split_features_target,
)


def save_error_analysis(model, splits, threshold: float = 0.60) -> None:
    ERROR_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    scores = predict_scores(model, splits.X_test)
    predictions = predictions_at_threshold(scores, threshold)

    errors = splits.X_test.copy()
    errors["actual_bad_review"] = splits.y_test.to_numpy()
    errors["predicted_bad_review"] = predictions
    errors["risk_score"] = scores
    errors["error_type"] = np.select(
        [
            (errors["actual_bad_review"] == 1) & (errors["predicted_bad_review"] == 1),
            (errors["actual_bad_review"] == 0) & (errors["predicted_bad_review"] == 0),
            (errors["actual_bad_review"] == 0) & (errors["predicted_bad_review"] == 1),
            (errors["actual_bad_review"] == 1) & (errors["predicted_bad_review"] == 0),
        ],
        ["true_positive", "true_negative", "false_positive", "false_negative"],
        default="unknown",
    )

    for error_type in ["true_positive", "false_positive", "false_negative"]:
        subset = errors[errors["error_type"] == error_type].copy()
        if error_type == "false_negative":
            subset = subset.sort_values("risk_score", ascending=False)
        else:
            subset = subset.sort_values("risk_score", ascending=False)
        subset.head(100).to_csv(ERROR_ANALYSIS_DIR / f"{error_type}_examples.csv", index=False)

    summary = (
        errors.groupby("error_type")
        .agg(
            orders=("risk_score", "size"),
            avg_risk_score=("risk_score", "mean"),
            avg_delivery_delay_days=("delivery_delay_days", "mean"),
            avg_delivery_time_days=("delivery_time_days", "mean"),
            avg_total_freight=("total_freight", "mean"),
            avg_payment_value=("payment_value", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(ERROR_ANALYSIS_DIR / "error_summary.csv", index=False)


def save_shap_importance(model, X_sample: pd.DataFrame) -> None:
    preprocessor = model.named_steps["preprocessor"]
    estimator = model.named_steps["model"]
    transformed = preprocessor.transform(X_sample)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    feature_names = preprocessor.get_feature_names_out()

    explainer = shap.TreeExplainer(estimator)
    shap_values = explainer.shap_values(transformed)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    shap_values = np.asarray(shap_values)
    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    importance = (
        pd.DataFrame(
            {
                "feature": feature_names,
                "mean_abs_shap": mean_abs_shap,
            }
        )
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )
    importance.to_csv(SHAP_IMPORTANCE_RESULTS, index=False)


def main() -> None:
    data = load_modeling_data(POST_DELIVERY_DATASET)
    X, y = split_features_target(data)
    splits = make_train_valid_test_split(X, y)
    model = joblib.load(ADVANCED_BEST_MODEL_PATH)

    save_error_analysis(model, splits, threshold=0.60)

    sample = splits.X_test.sample(
        n=min(1500, len(splits.X_test)),
        random_state=RANDOM_STATE,
    )
    save_shap_importance(model, sample)

    print(f"Saved error analysis to {ERROR_ANALYSIS_DIR}")
    print(f"Saved SHAP importance to {SHAP_IMPORTANCE_RESULTS}")


if __name__ == "__main__":
    main()
