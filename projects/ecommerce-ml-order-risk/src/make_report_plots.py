import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    ADVANCED_RESULTS,
    ADVANCED_THRESHOLD_RESULTS,
    BUSINESS_THRESHOLD_RESULTS,
    FEATURE_IMPORTANCE_RESULTS,
    LEARNING_CURVE_RESULTS,
    PRECISION_POLICY_RESULTS,
    REPORTS_DIR,
    THRESHOLD_RESULTS,
    TIME_VALIDATION_RESULTS,
    TUNED_RESULTS,
)


def save_threshold_tradeoff_plot() -> None:
    thresholds = pd.read_csv(THRESHOLD_RESULTS)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(thresholds["threshold"], thresholds["precision"], marker="o", label="Precision")
    ax.plot(thresholds["threshold"], thresholds["recall"], marker="o", label="Recall")
    ax.plot(thresholds["threshold"], thresholds["f1"], marker="o", label="F1")
    ax.plot(
        thresholds["threshold"],
        thresholds["flagged_order_rate"],
        marker="o",
        label="Flagged order rate",
    )
    ax.set_title("Threshold Tradeoff for Bad Review Risk Model")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score / rate")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "threshold_tradeoff.png", dpi=180)
    plt.close(fig)


def save_feature_importance_plot() -> None:
    importance = pd.read_csv(FEATURE_IMPORTANCE_RESULTS).head(20)
    importance = importance.iloc[::-1].copy()
    importance["feature"] = (
        importance["feature"]
        .str.replace("numeric__", "", regex=False)
        .str.replace("categorical__", "", regex=False)
    )

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(importance["feature"], importance["importance"])
    ax.set_title("Top 20 LightGBM Feature Importances")
    ax.set_xlabel("Importance")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "feature_importance_top20.png", dpi=180)
    plt.close(fig)


def save_tuned_model_comparison_plot() -> None:
    tuned = pd.read_csv(TUNED_RESULTS)
    validation = tuned[tuned["split"] == "validation"].copy()
    best_by_model = (
        validation.sort_values("pr_auc", ascending=False)
        .groupby("model", as_index=False)
        .first()
        .sort_values("pr_auc")
    )

    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.barh(best_by_model["model"], best_by_model["pr_auc"])
    ax.set_title("Best Tuned Candidate by Model Family")
    ax.set_xlabel("Validation PR-AUC")
    ax.set_xlim(0, max(0.65, best_by_model["pr_auc"].max() + 0.03))
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "tuned_model_pr_auc.png", dpi=180)
    plt.close(fig)


def save_advanced_model_comparison_plot() -> None:
    advanced = pd.read_csv(ADVANCED_RESULTS)
    test = advanced[advanced["split"] == "test"].copy()
    test["label"] = test["dataset_mode"] + " / " + test["model"]
    test = test.sort_values("pr_auc")

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(test["label"], test["pr_auc"])
    ax.set_title("Advanced Experiment Test PR-AUC")
    ax.set_xlabel("Test PR-AUC")
    ax.set_xlim(0, max(0.65, test["pr_auc"].max() + 0.03))
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "advanced_model_pr_auc.png", dpi=180)
    plt.close(fig)


def save_advanced_threshold_tradeoff_plot() -> None:
    thresholds = pd.read_csv(ADVANCED_THRESHOLD_RESULTS)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(thresholds["threshold"], thresholds["precision"], marker="o", label="Precision")
    ax.plot(thresholds["threshold"], thresholds["recall"], marker="o", label="Recall")
    ax.plot(thresholds["threshold"], thresholds["f1"], marker="o", label="F1")
    ax.plot(
        thresholds["threshold"],
        thresholds["flagged_order_rate"],
        marker="o",
        label="Flagged order rate",
    )
    ax.set_title("Advanced LightGBM Threshold Tradeoff")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score / rate")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "advanced_threshold_tradeoff.png", dpi=180)
    plt.close(fig)


def save_learning_curve_plot() -> None:
    learning_curve = pd.read_csv(LEARNING_CURVE_RESULTS)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(
        learning_curve["train_fraction"],
        learning_curve["train_pr_auc"],
        marker="o",
        label="Training PR-AUC",
    )
    ax.plot(
        learning_curve["train_fraction"],
        learning_curve["holdout_pr_auc"],
        marker="o",
        label="Holdout PR-AUC",
    )
    ax.plot(
        learning_curve["train_fraction"],
        learning_curve["generalization_gap"],
        marker="o",
        label="Generalization gap",
    )
    ax.set_title("Learning Curve and Overfitting Gap")
    ax.set_xlabel("Training data fraction")
    ax.set_ylabel("PR-AUC")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "learning_curve.png", dpi=180)
    plt.close(fig)


def save_time_validation_plot() -> None:
    time_results = pd.read_csv(TIME_VALIDATION_RESULTS)
    test_results = time_results[time_results["split"] == "test"].sort_values("pr_auc")

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(test_results["model"], test_results["pr_auc"])
    ax.set_title("Future-Period Test PR-AUC by Model")
    ax.set_xlabel("Test PR-AUC")
    ax.set_xlim(0, max(0.5, test_results["pr_auc"].max() + 0.04))
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "time_validation_pr_auc.png", dpi=180)
    plt.close(fig)


def save_business_threshold_plot() -> None:
    thresholds = pd.read_csv(BUSINESS_THRESHOLD_RESULTS)

    fig, ax1 = plt.subplots(figsize=(9, 5.2))
    ax1.plot(
        thresholds["threshold"],
        thresholds["estimated_savings_vs_no_model"],
        marker="o",
        color="#1f77b4",
        label="Estimated savings",
    )
    ax1.set_title("Business Threshold Tradeoff")
    ax1.set_xlabel("Decision threshold")
    ax1.set_ylabel("Estimated savings vs no model")
    ax1.grid(alpha=0.25)

    ax2 = ax1.twinx()
    ax2.plot(
        thresholds["threshold"],
        thresholds["flagged_order_rate"],
        marker="o",
        color="#d62728",
        label="Flagged order rate",
    )
    ax2.set_ylabel("Flagged order rate")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="best")

    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "business_threshold_tradeoff.png", dpi=180)
    plt.close(fig)


def save_precision_policy_plot() -> None:
    policies = pd.read_csv(PRECISION_POLICY_RESULTS)
    policies = policies[
        (policies["target"] == "bad_review")
        & policies["test_precision"].notna()
        & policies["policy"].str.contains("0.25|0.35|top_5pct|top_10pct", regex=True)
    ].copy()
    policies["label"] = policies["model"].str.replace("_lightgbm", "", regex=False) + "\n" + policies[
        "policy"
    ].str.replace("max_precision_with_validation_recall_at_least_", "recall >= ", regex=False).str.replace(
        "review_top_", "top ", regex=False
    ).str.replace(
        "_highest_risk_orders", "", regex=False
    )

    policies = policies.sort_values("test_precision", ascending=True)

    fig, ax = plt.subplots(figsize=(9.5, 6))
    ax.barh(policies["label"], policies["test_precision"], label="Precision")
    ax.scatter(policies["test_recall"], policies["label"], color="#d62728", label="Recall", zorder=3)
    ax.set_title("High-Precision Operating Policies")
    ax.set_xlabel("Test precision / recall")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "precision_policy_tradeoff.png", dpi=180)
    plt.close(fig)


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    save_threshold_tradeoff_plot()
    save_feature_importance_plot()
    save_tuned_model_comparison_plot()
    if ADVANCED_RESULTS.exists():
        save_advanced_model_comparison_plot()
    if ADVANCED_THRESHOLD_RESULTS.exists():
        save_advanced_threshold_tradeoff_plot()
    if LEARNING_CURVE_RESULTS.exists():
        save_learning_curve_plot()
    if TIME_VALIDATION_RESULTS.exists():
        save_time_validation_plot()
    if BUSINESS_THRESHOLD_RESULTS.exists():
        save_business_threshold_plot()
    if PRECISION_POLICY_RESULTS.exists():
        save_precision_policy_plot()
    print(f"Saved plots to {REPORTS_DIR}")


if __name__ == "__main__":
    main()
