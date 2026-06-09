from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import joblib
import pandas as pd
from sklearn.base import clone
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from config import (
    BEST_MODEL_PATH,
    FEATURE_IMPORTANCE_RESULTS,
    MODELS_DIR,
    RANDOM_STATE,
    REPORTS_DIR,
    THRESHOLD_RESULTS,
    TUNED_RESULTS,
)
from modeling_utils import (
    build_preprocessor,
    get_model_scores,
    load_modeling_data,
    make_train_valid_test_split,
    predict_scores,
    predictions_at_threshold,
    split_features_target,
)


def parameter_grid(grid: dict) -> list[dict]:
    keys = list(grid.keys())
    return [dict(zip(keys, values)) for values in product(*(grid[key] for key in keys))]


def get_candidate_models(positive_weight: float) -> dict:
    return {
        "Random Forest": {
            "estimator": RandomForestClassifier(
                class_weight="balanced_subsample",
                n_jobs=-1,
                random_state=RANDOM_STATE,
            ),
            "params": parameter_grid(
                {
                    "model__n_estimators": [200, 350],
                    "model__max_depth": [10, 16, None],
                    "model__min_samples_leaf": [5, 10],
                }
            ),
        },
        "XGBoost": {
            "estimator": XGBClassifier(
                eval_metric="logloss",
                scale_pos_weight=positive_weight,
                random_state=RANDOM_STATE,
            ),
            "params": parameter_grid(
                {
                    "model__n_estimators": [220, 350],
                    "model__max_depth": [3, 5],
                    "model__learning_rate": [0.04, 0.08],
                    "model__subsample": [0.85],
                    "model__colsample_bytree": [0.85],
                }
            ),
        },
        "LightGBM": {
            "estimator": LGBMClassifier(
                class_weight="balanced",
                random_state=RANDOM_STATE,
                verbose=-1,
            ),
            "params": parameter_grid(
                {
                    "model__n_estimators": [220, 350],
                    "model__num_leaves": [31, 63],
                    "model__learning_rate": [0.04, 0.08],
                    "model__min_child_samples": [20, 60],
                }
            ),
        },
    }


def train_and_score_candidates(splits):
    positive_weight = (len(splits.y_train) - splits.y_train.sum()) / splits.y_train.sum()
    preprocessor = build_preprocessor(splits.X_train)
    candidate_models = get_candidate_models(positive_weight)
    all_results = []
    best = None

    for model_name, config in candidate_models.items():
        for candidate_number, params in enumerate(config["params"], start=1):
            print(f"Training {model_name} candidate {candidate_number}/{len(config['params'])}")
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", clone(preprocessor)),
                    ("model", clone(config["estimator"])),
                ]
            )
            pipeline.set_params(**params)
            pipeline.fit(splits.X_train, splits.y_train)

            valid_scores = predict_scores(pipeline, splits.X_valid)
            valid_predictions = predictions_at_threshold(valid_scores, 0.5)
            metrics = get_model_scores(splits.y_valid, valid_predictions, valid_scores)
            row = {
                "model": model_name,
                "candidate": candidate_number,
                "params": json.dumps(params, sort_keys=True),
                "split": "validation",
                **metrics,
            }
            all_results.append(row)

            if best is None or row["pr_auc"] > best["row"]["pr_auc"]:
                best = {"name": model_name, "pipeline": pipeline, "row": row, "params": params}

    return best, pd.DataFrame(all_results)


def evaluate_best_on_test(best, splits) -> dict:
    test_scores = predict_scores(best["pipeline"], splits.X_test)
    test_predictions = predictions_at_threshold(test_scores, 0.5)
    return {
        "model": best["name"],
        "candidate": best["row"]["candidate"],
        "params": json.dumps(best["params"], sort_keys=True),
        "split": "test",
        **get_model_scores(splits.y_test, test_predictions, test_scores),
    }


def build_threshold_analysis(best_pipeline, X_test, y_test) -> pd.DataFrame:
    scores = predict_scores(best_pipeline, X_test)
    rows = []
    for threshold in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70]:
        predictions = predictions_at_threshold(scores, threshold)
        metrics = get_model_scores(y_test, predictions, scores)
        flagged_rate = predictions.mean()
        rows.append(
            {
                "threshold": threshold,
                "flagged_order_rate": flagged_rate,
                **metrics,
            }
        )
    return pd.DataFrame(rows)


def get_feature_names(pipeline: Pipeline) -> list[str]:
    preprocessor = pipeline.named_steps["preprocessor"]
    return preprocessor.get_feature_names_out().tolist()


def save_feature_importance(best_pipeline: Pipeline) -> None:
    estimator = best_pipeline.named_steps["model"]
    if not hasattr(estimator, "feature_importances_"):
        return
    feature_names = get_feature_names(best_pipeline)
    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": estimator.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    importance.to_csv(FEATURE_IMPORTANCE_RESULTS, index=False)


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_modeling_data()
    X, y = split_features_target(data)
    splits = make_train_valid_test_split(X, y)

    best, validation_results = train_and_score_candidates(splits)
    test_result = evaluate_best_on_test(best, splits)

    results = pd.concat([validation_results, pd.DataFrame([test_result])], ignore_index=True)
    results = results.sort_values(["split", "pr_auc"], ascending=[True, False])
    results.to_csv(TUNED_RESULTS, index=False)

    threshold_results = build_threshold_analysis(best["pipeline"], splits.X_test, splits.y_test)
    threshold_results.to_csv(THRESHOLD_RESULTS, index=False)

    save_feature_importance(best["pipeline"])
    joblib.dump(best["pipeline"], BEST_MODEL_PATH)

    print("Best validation model:")
    print(pd.DataFrame([best["row"]]).round(4).to_string(index=False))
    print("\nTest result:")
    print(pd.DataFrame([test_result]).round(4).to_string(index=False))
    print(f"\nSaved tuned results to {TUNED_RESULTS}")
    print(f"Saved threshold analysis to {THRESHOLD_RESULTS}")
    print(f"Saved best model to {BEST_MODEL_PATH}")
    if FEATURE_IMPORTANCE_RESULTS.exists():
        print(f"Saved feature importance to {FEATURE_IMPORTANCE_RESULTS}")


if __name__ == "__main__":
    main()
