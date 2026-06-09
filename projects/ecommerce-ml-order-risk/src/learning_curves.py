import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline

from config import LEARNING_CURVE_RESULTS, MODEL_DATASET, RANDOM_STATE, REPORTS_DIR
from modeling_utils import build_preprocessor, load_modeling_data, predict_scores, split_features_target


TRAIN_FRACTIONS = [0.10, 0.25, 0.50, 0.75, 1.00]


def get_regularized_lightgbm() -> LGBMClassifier:
    return LGBMClassifier(
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
    )


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = load_modeling_data(MODEL_DATASET)
    X, y = split_features_target(data)

    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_STATE)
    train_valid_idx, holdout_idx = next(splitter.split(X, y))
    X_train_valid = X.iloc[train_valid_idx]
    y_train_valid = y.iloc[train_valid_idx]
    X_holdout = X.iloc[holdout_idx]
    y_holdout = y.iloc[holdout_idx]

    rows = []
    for fraction in TRAIN_FRACTIONS:
        if fraction < 1.0:
            sub_splitter = StratifiedShuffleSplit(
                n_splits=1,
                train_size=fraction,
                random_state=RANDOM_STATE,
            )
            sub_idx, _ = next(sub_splitter.split(X_train_valid, y_train_valid))
            X_train = X_train_valid.iloc[sub_idx]
            y_train = y_train_valid.iloc[sub_idx]
        else:
            X_train = X_train_valid
            y_train = y_train_valid

        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(X_train)),
                ("model", get_regularized_lightgbm()),
            ]
        )
        pipeline.fit(X_train, y_train)

        train_scores = predict_scores(pipeline, X_train)
        holdout_scores = predict_scores(pipeline, X_holdout)

        rows.append(
            {
                "train_fraction": fraction,
                "train_rows": len(X_train),
                "train_pr_auc": average_precision_score(y_train, train_scores),
                "holdout_pr_auc": average_precision_score(y_holdout, holdout_scores),
                "generalization_gap": average_precision_score(y_train, train_scores)
                - average_precision_score(y_holdout, holdout_scores),
            }
        )
        print(f"Finished fraction {fraction:.2f}")

    results = pd.DataFrame(rows)
    results.to_csv(LEARNING_CURVE_RESULTS, index=False)
    print(results.round(4).to_string(index=False))
    print(f"Saved learning curve results to {LEARNING_CURVE_RESULTS}")


if __name__ == "__main__":
    main()

