from __future__ import annotations

import json

import joblib
import optuna
import pandas as pd
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import brier_score_loss
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from config import (
    ADVANCED_BEST_MODEL_PATH,
    ADVANCED_RESULTS,
    ADVANCED_THRESHOLD_RESULTS,
    CALIBRATION_RESULTS,
    POST_DELIVERY_DATASET,
    PRE_DELIVERY_DATASET,
    RANDOM_STATE,
    REPORTS_DIR,
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


N_TRIALS = 6
THRESHOLDS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]


def make_model(model_name: str, trial: optuna.Trial, positive_weight: float):
    if model_name == "LightGBM":
        return LGBMClassifier(
            n_estimators=trial.suggest_int("n_estimators", 250, 650),
            learning_rate=trial.suggest_float("learning_rate", 0.015, 0.09, log=True),
            num_leaves=trial.suggest_categorical("num_leaves", [15, 31, 63, 95]),
            min_child_samples=trial.suggest_int("min_child_samples", 20, 120),
            subsample=trial.suggest_float("subsample", 0.75, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.75, 1.0),
            reg_lambda=trial.suggest_float("reg_lambda", 0.0, 8.0),
            class_weight="balanced",
            random_state=RANDOM_STATE,
            verbose=-1,
        )

    if model_name == "XGBoost":
        return XGBClassifier(
            n_estimators=trial.suggest_int("n_estimators", 250, 650),
            max_depth=trial.suggest_int("max_depth", 3, 7),
            learning_rate=trial.suggest_float("learning_rate", 0.015, 0.09, log=True),
            subsample=trial.suggest_float("subsample", 0.75, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.75, 1.0),
            min_child_weight=trial.suggest_int("min_child_weight", 1, 8),
            reg_lambda=trial.suggest_float("reg_lambda", 0.0, 8.0),
            scale_pos_weight=positive_weight,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
        )

    if model_name == "CatBoost":
        return CatBoostClassifier(
            iterations=trial.suggest_int("iterations", 250, 650),
            depth=trial.suggest_int("depth", 4, 8),
            learning_rate=trial.suggest_float("learning_rate", 0.015, 0.09, log=True),
            l2_leaf_reg=trial.suggest_float("l2_leaf_reg", 1.0, 12.0),
            auto_class_weights="Balanced",
            loss_function="Logloss",
            eval_metric="PRAUC",
            random_seed=RANDOM_STATE,
            verbose=False,
        )

    raise ValueError(f"Unsupported model: {model_name}")


def objective(model_name: str, splits, positive_weight: float):
    def _objective(trial: optuna.Trial) -> float:
        model = make_model(model_name, trial, positive_weight)
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(splits.X_train)),
                ("model", model),
            ]
        )
        pipeline.fit(splits.X_train, splits.y_train)
        scores = predict_scores(pipeline, splits.X_valid)
        predictions = predictions_at_threshold(scores, 0.5)
        metrics = get_model_scores(splits.y_valid, predictions, scores)
        trial.set_user_attr("metrics", metrics)
        return metrics["pr_auc"]

    return _objective


def tune_dataset(dataset_name: str, dataset_path):
    print(f"\n=== Dataset mode: {dataset_name} ===")
    data = load_modeling_data(dataset_path)
    X, y = split_features_target(data)
    splits = make_train_valid_test_split(X, y)
    positive_weight = (len(splits.y_train) - splits.y_train.sum()) / splits.y_train.sum()

    rows = []
    best = None

    for model_name in ["LightGBM", "XGBoost", "CatBoost"]:
        print(f"Tuning {model_name} on {dataset_name}")
        study = optuna.create_study(direction="maximize")
        study.optimize(objective(model_name, splits, positive_weight), n_trials=N_TRIALS)

        best_trial = study.best_trial
        best_model = make_model(model_name, best_trial, positive_weight)
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(splits.X_train)),
                ("model", best_model),
            ]
        )
        pipeline.fit(splits.X_train, splits.y_train)

        valid_scores = predict_scores(pipeline, splits.X_valid)
        valid_predictions = predictions_at_threshold(valid_scores, 0.5)
        valid_metrics = get_model_scores(splits.y_valid, valid_predictions, valid_scores)

        test_scores = predict_scores(pipeline, splits.X_test)
        test_predictions = predictions_at_threshold(test_scores, 0.5)
        test_metrics = get_model_scores(splits.y_test, test_predictions, test_scores)

        for split_name, metrics in [("validation", valid_metrics), ("test", test_metrics)]:
            rows.append(
                {
                    "dataset_mode": dataset_name,
                    "model": model_name,
                    "split": split_name,
                    "params": json.dumps(best_trial.params, sort_keys=True),
                    **metrics,
                }
            )

        if best is None or valid_metrics["pr_auc"] > best["valid_metrics"]["pr_auc"]:
            best = {
                "dataset_name": dataset_name,
                "model_name": model_name,
                "pipeline": pipeline,
                "splits": splits,
                "params": best_trial.params,
                "valid_metrics": valid_metrics,
                "test_metrics": test_metrics,
            }

    return best, rows


def build_threshold_rows(best) -> list[dict]:
    scores = predict_scores(best["pipeline"], best["splits"].X_test)
    rows = []
    for threshold in THRESHOLDS:
        predictions = predictions_at_threshold(scores, threshold)
        rows.append(
            {
                "dataset_mode": best["dataset_name"],
                "model": best["model_name"],
                "threshold": threshold,
                "flagged_order_rate": predictions.mean(),
                **get_model_scores(best["splits"].y_test, predictions, scores),
            }
        )
    return rows


def calibrate_best_model(best) -> dict:
    base_pipeline = clone(best["pipeline"])
    base_pipeline.fit(best["splits"].X_train, best["splits"].y_train)

    calibrated = CalibratedClassifierCV(
        FrozenEstimator(base_pipeline),
        method="isotonic",
    )
    calibrated.fit(best["splits"].X_valid, best["splits"].y_valid)

    raw_scores = predict_scores(base_pipeline, best["splits"].X_test)
    calibrated_scores = calibrated.predict_proba(best["splits"].X_test)[:, 1]

    return {
        "dataset_mode": best["dataset_name"],
        "model": best["model_name"],
        "raw_brier_score": brier_score_loss(best["splits"].y_test, raw_scores),
        "calibrated_brier_score": brier_score_loss(best["splits"].y_test, calibrated_scores),
        "raw_pr_auc": get_model_scores(
            best["splits"].y_test,
            predictions_at_threshold(raw_scores, 0.5),
            raw_scores,
        )["pr_auc"],
        "calibrated_pr_auc": get_model_scores(
            best["splits"].y_test,
            predictions_at_threshold(calibrated_scores, 0.5),
            calibrated_scores,
        )["pr_auc"],
    }


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    all_rows = []
    best_models = []
    for dataset_name, dataset_path in [
        ("pre_delivery", PRE_DELIVERY_DATASET),
        ("post_delivery", POST_DELIVERY_DATASET),
    ]:
        best, rows = tune_dataset(dataset_name, dataset_path)
        all_rows.extend(rows)
        best_models.append(best)

    best_overall = max(best_models, key=lambda item: item["valid_metrics"]["pr_auc"])

    pd.DataFrame(all_rows).sort_values(
        ["split", "pr_auc"],
        ascending=[True, False],
    ).to_csv(ADVANCED_RESULTS, index=False)

    pd.DataFrame(build_threshold_rows(best_overall)).to_csv(
        ADVANCED_THRESHOLD_RESULTS,
        index=False,
    )

    calibration = calibrate_best_model(best_overall)
    pd.DataFrame([calibration]).to_csv(CALIBRATION_RESULTS, index=False)

    joblib.dump(best_overall["pipeline"], ADVANCED_BEST_MODEL_PATH)

    print("\nBest overall model:")
    print(
        pd.DataFrame(
            [
                {
                    "dataset_mode": best_overall["dataset_name"],
                    "model": best_overall["model_name"],
                    "params": json.dumps(best_overall["params"], sort_keys=True),
                    **best_overall["test_metrics"],
                }
            ]
        )
        .round(4)
        .to_string(index=False)
    )
    print(f"\nSaved advanced results to {ADVANCED_RESULTS}")
    print(f"Saved threshold analysis to {ADVANCED_THRESHOLD_RESULTS}")
    print(f"Saved calibration results to {CALIBRATION_RESULTS}")
    print(f"Saved model to {ADVANCED_BEST_MODEL_PATH}")


if __name__ == "__main__":
    main()
