from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import MODEL_DATASET, RANDOM_STATE, TARGET_COLUMN


DROP_FROM_FEATURES = [TARGET_COLUMN, "review_score", "order_id"]


@dataclass(frozen=True)
class DatasetSplits:
    X_train: pd.DataFrame
    X_valid: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_valid: pd.Series
    y_test: pd.Series


def load_modeling_data(path=MODEL_DATASET) -> pd.DataFrame:
    return pd.read_csv(path)


def make_feature_matrix(data: pd.DataFrame) -> pd.DataFrame:
    extra_drops = [column for column in ["order_purchase_timestamp"] if column in data.columns]
    available_drops = [column for column in DROP_FROM_FEATURES + extra_drops if column in data.columns]
    return data.drop(columns=available_drops)


def split_features_target(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    y = data[TARGET_COLUMN]
    X = make_feature_matrix(data)
    return X, y


def make_train_valid_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    valid_size: float = 0.2,
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
) -> DatasetSplits:
    X_train_valid, X_test, y_train_valid, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    relative_valid_size = valid_size / (1 - test_size)
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_valid,
        y_train_valid,
        test_size=relative_valid_size,
        random_state=random_state,
        stratify=y_train_valid,
    )
    return DatasetSplits(X_train, X_valid, X_test, y_train, y_valid, y_test)


def make_time_based_split(
    data: pd.DataFrame,
    timestamp_column: str = "order_purchase_timestamp",
    train_size: float = 0.6,
    valid_size: float = 0.2,
) -> DatasetSplits:
    ordered = data.sort_values(timestamp_column).reset_index(drop=True)
    train_end = int(len(ordered) * train_size)
    valid_end = int(len(ordered) * (train_size + valid_size))

    train = ordered.iloc[:train_end].copy()
    valid = ordered.iloc[train_end:valid_end].copy()
    test = ordered.iloc[valid_end:].copy()

    X_train, y_train = split_features_target(train)
    X_valid, y_valid = split_features_target(valid)
    X_test, y_test = split_features_target(test)
    return DatasetSplits(X_train, X_valid, X_test, y_train, y_valid, y_test)


def build_preprocessor(X: pd.DataFrame, dense: bool = False) -> ColumnTransformer:
    categorical = X.select_dtypes(include=["object", "str", "category"]).columns.tolist()
    numeric = [column for column in X.columns if column not in categorical]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    min_frequency=20,
                    sparse_output=not dense,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipe, numeric),
            ("categorical", categorical_pipe, categorical),
        ]
    )


def get_model_scores(y_true, predictions, scores) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, predictions).ravel()
    return {
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "f1": f1_score(y_true, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_true, scores),
        "pr_auc": average_precision_score(y_true, scores),
        "brier_score": brier_score_loss(y_true, scores),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def predict_scores(model, X):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    if hasattr(model, "decision_function"):
        return model.decision_function(X)
    return model.predict(X)


def predictions_at_threshold(scores, threshold: float):
    return (scores >= threshold).astype(int)
