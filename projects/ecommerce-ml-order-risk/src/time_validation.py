import json

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

from config import RANDOM_STATE, REPORTS_DIR, TEMPORAL_DATASET, TIME_VALIDATION_RESULTS
from modeling_utils import (
    build_preprocessor,
    get_model_scores,
    load_modeling_data,
    make_time_based_split,
    predict_scores,
    predictions_at_threshold,
)


def get_models(positive_weight: float) -> dict:
    return {
        "LightGBM": LGBMClassifier(
            n_estimators=431,
            learning_rate=0.030516595026498134,
            num_leaves=31,
            min_child_samples=109,
            subsample=0.9249007225175158,
            colsample_bytree=0.8583625150859961,
            reg_lambda=0.6782624410275622,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            verbose=-1,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=554,
            max_depth=7,
            learning_rate=0.019580801905990514,
            subsample=0.8119909178573812,
            colsample_bytree=0.8929915047648647,
            min_child_weight=4,
            reg_lambda=4.765743953080102,
            scale_pos_weight=positive_weight,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
        ),
        "CatBoost": CatBoostClassifier(
            iterations=545,
            depth=8,
            learning_rate=0.04240896145458551,
            l2_leaf_reg=10.95828358151894,
            auto_class_weights="Balanced",
            loss_function="Logloss",
            eval_metric="PRAUC",
            random_seed=RANDOM_STATE,
            verbose=False,
        ),
    }


def score_time_model(name: str, estimator, splits) -> dict:
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(splits.X_train)),
            ("model", estimator),
        ]
    )
    pipeline.fit(splits.X_train, splits.y_train)

    rows = []
    for split_name, X_split, y_split in [
        ("train", splits.X_train, splits.y_train),
        ("validation", splits.X_valid, splits.y_valid),
        ("test", splits.X_test, splits.y_test),
    ]:
        scores = predict_scores(pipeline, X_split)
        predictions = predictions_at_threshold(scores, 0.5)
        rows.append(
            {
                "model": name,
                "split": split_name,
                **get_model_scores(y_split, predictions, scores),
            }
        )
    return rows


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = load_modeling_data(TEMPORAL_DATASET)
    splits = make_time_based_split(data)
    positive_weight = (len(splits.y_train) - splits.y_train.sum()) / splits.y_train.sum()

    rows = []
    for name, estimator in get_models(positive_weight).items():
        print(f"Training time-based {name}")
        rows.extend(score_time_model(name, estimator, splits))

    results = pd.DataFrame(rows)
    results.to_csv(TIME_VALIDATION_RESULTS, index=False)
    print(results.round(4).to_string(index=False))
    print(f"Saved time validation results to {TIME_VALIDATION_RESULTS}")


if __name__ == "__main__":
    main()

