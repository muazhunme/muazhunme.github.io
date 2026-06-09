import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from config import BASELINE_RESULTS, MODEL_DATASET, RANDOM_STATE, REPORTS_DIR, TARGET_COLUMN
from modeling_utils import build_preprocessor, get_model_scores, predict_scores


def score_model(name: str, model, X_train, X_test, y_train, y_test) -> dict:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    scores = predict_scores(model, X_test)
    return {"model": name, **get_model_scores(y_test, predictions, scores)}


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(MODEL_DATASET)
    y = data[TARGET_COLUMN]
    X = data.drop(columns=[TARGET_COLUMN, "review_score", "order_id"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    preprocessor = build_preprocessor(X)
    positive_weight = (len(y_train) - y_train.sum()) / y_train.sum()

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=250,
            min_samples_leaf=8,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
        "KNN": KNeighborsClassifier(n_neighbors=21),
        "Linear SVM": LinearSVC(
            class_weight="balanced",
            random_state=RANDOM_STATE,
            max_iter=5000,
        ),
        "Naive Bayes": GaussianNB(),
        "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "XGBoost": XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.06,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            scale_pos_weight=positive_weight,
            random_state=RANDOM_STATE,
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=250,
            learning_rate=0.06,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            verbose=-1,
        ),
    }

    results = []
    for name, estimator in models.items():
        print(f"Training {name}...")
        if name == "Naive Bayes":
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", build_preprocessor(X, dense=True)),
                    ("model", estimator),
                ]
            )
        else:
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("model", estimator),
                ]
            )
        results.append(score_model(name, pipeline, X_train, X_test, y_train, y_test))

    results_df = pd.DataFrame(results).sort_values("pr_auc", ascending=False)
    results_df.to_csv(BASELINE_RESULTS, index=False)
    print(results_df.round(4).to_string(index=False))
    print(f"Saved results to {BASELINE_RESULTS}")


if __name__ == "__main__":
    main()
