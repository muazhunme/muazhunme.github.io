import json

import joblib
import optuna
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.base import clone
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline

from config import CV_BEST_MODEL_PATH, CV_TUNING_RESULTS, MODEL_DATASET, RANDOM_STATE, REPORTS_DIR
from modeling_utils import (
    build_preprocessor,
    get_model_scores,
    load_modeling_data,
    predict_scores,
    predictions_at_threshold,
    split_features_target,
)


N_TRIALS = 20
N_SPLITS = 4


def make_lightgbm(trial: optuna.Trial) -> LGBMClassifier:
    return LGBMClassifier(
        n_estimators=trial.suggest_int("n_estimators", 250, 900),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.08, log=True),
        num_leaves=trial.suggest_categorical("num_leaves", [15, 31, 63]),
        max_depth=trial.suggest_categorical("max_depth", [-1, 4, 6, 8, 10]),
        min_child_samples=trial.suggest_int("min_child_samples", 40, 180),
        subsample=trial.suggest_float("subsample", 0.70, 1.0),
        colsample_bytree=trial.suggest_float("colsample_bytree", 0.70, 1.0),
        reg_alpha=trial.suggest_float("reg_alpha", 0.0, 6.0),
        reg_lambda=trial.suggest_float("reg_lambda", 0.0, 10.0),
        min_split_gain=trial.suggest_float("min_split_gain", 0.0, 0.20),
        class_weight="balanced",
        random_state=RANDOM_STATE,
        verbose=-1,
    )


def objective(X_train_valid, y_train_valid):
    def _objective(trial: optuna.Trial) -> float:
        cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
        fold_scores = []

        for fold, (train_idx, valid_idx) in enumerate(cv.split(X_train_valid, y_train_valid), start=1):
            X_train_fold = X_train_valid.iloc[train_idx]
            y_train_fold = y_train_valid.iloc[train_idx]
            X_valid_fold = X_train_valid.iloc[valid_idx]
            y_valid_fold = y_train_valid.iloc[valid_idx]

            pipeline = Pipeline(
                steps=[
                    ("preprocessor", build_preprocessor(X_train_fold)),
                    ("model", make_lightgbm(trial)),
                ]
            )
            pipeline.fit(X_train_fold, y_train_fold)
            scores = predict_scores(pipeline, X_valid_fold)
            fold_scores.append(average_precision_score(y_valid_fold, scores))

        mean_score = float(pd.Series(fold_scores).mean())
        std_score = float(pd.Series(fold_scores).std())
        trial.set_user_attr("fold_pr_auc", fold_scores)
        trial.set_user_attr("mean_pr_auc", mean_score)
        trial.set_user_attr("std_pr_auc", std_score)
        return mean_score

    return _objective


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_modeling_data(MODEL_DATASET)
    X, y = split_features_target(data)
    X_train_valid, X_test, y_train_valid, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    study = optuna.create_study(direction="maximize")
    study.optimize(objective(X_train_valid, y_train_valid), n_trials=N_TRIALS)

    rows = []
    for trial in study.trials:
        rows.append(
            {
                "trial": trial.number,
                "mean_cv_pr_auc": trial.user_attrs.get("mean_pr_auc"),
                "std_cv_pr_auc": trial.user_attrs.get("std_pr_auc"),
                "params": json.dumps(trial.params, sort_keys=True),
            }
        )

    best_params = study.best_trial.params
    final_model = LGBMClassifier(
        **best_params,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        verbose=-1,
    )
    final_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(X_train_valid)),
            ("model", final_model),
        ]
    )
    final_pipeline.fit(X_train_valid, y_train_valid)

    test_scores = predict_scores(final_pipeline, X_test)
    test_predictions = predictions_at_threshold(test_scores, 0.5)
    test_metrics = get_model_scores(y_test, test_predictions, test_scores)

    rows.append(
        {
            "trial": "final_test",
            "mean_cv_pr_auc": study.best_value,
            "std_cv_pr_auc": study.best_trial.user_attrs.get("std_pr_auc"),
            "params": json.dumps(best_params, sort_keys=True),
            **test_metrics,
        }
    )

    pd.DataFrame(rows).to_csv(CV_TUNING_RESULTS, index=False)
    joblib.dump(final_pipeline, CV_BEST_MODEL_PATH)

    print("Best CV params:")
    print(json.dumps(best_params, indent=2, sort_keys=True))
    print("\nFinal test metrics:")
    print(pd.DataFrame([test_metrics]).round(4).to_string(index=False))
    print(f"\nSaved CV tuning results to {CV_TUNING_RESULTS}")
    print(f"Saved CV tuned model to {CV_BEST_MODEL_PATH}")


if __name__ == "__main__":
    main()

