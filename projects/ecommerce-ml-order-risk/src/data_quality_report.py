import pandas as pd

from config import (
    DATA_QUALITY_MISSING_VALUES,
    DATA_QUALITY_REPORT,
    MODEL_DATASET,
    REPORTS_DIR,
    TARGET_COLUMN,
    TEMPORAL_DATASET,
)


def format_percent(value: float) -> str:
    return f"{value:.2%}"


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(MODEL_DATASET)

    temporal_data = None
    if TEMPORAL_DATASET.exists():
        temporal_data = pd.read_csv(TEMPORAL_DATASET, usecols=["order_purchase_timestamp"])
        temporal_data["order_purchase_timestamp"] = pd.to_datetime(
            temporal_data["order_purchase_timestamp"],
            errors="coerce",
        )

    missing = (
        data.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_count"})
    )
    missing["missing_rate"] = missing["missing_count"] / len(data)
    missing = missing.sort_values(["missing_count", "column"], ascending=[False, True])
    missing.to_csv(DATA_QUALITY_MISSING_VALUES, index=False)

    duplicate_order_ids = int(data["order_id"].duplicated().sum()) if "order_id" in data.columns else 0
    target_rate = float(data[TARGET_COLUMN].mean())
    target_count = int(data[TARGET_COLUMN].sum())
    numeric_count = len(data.select_dtypes(include=["number", "bool"]).columns)
    categorical_count = len(data.select_dtypes(include=["object", "str", "category"]).columns)

    top_missing = missing[missing["missing_count"] > 0].head(15)
    if top_missing.empty:
        missing_section = "No missing values were found in the modeling dataset."
    else:
        lines = ["| Column | Missing Count | Missing Rate |", "|---|---:|---:|"]
        for row in top_missing.itertuples(index=False):
            lines.append(f"| {row.column} | {row.missing_count:,} | {row.missing_rate:.2%} |")
        missing_section = "\n".join(lines)

    date_section = "Date range unavailable because the temporal dataset was not found."
    if temporal_data is not None:
        min_date = temporal_data["order_purchase_timestamp"].min()
        max_date = temporal_data["order_purchase_timestamp"].max()
        date_section = f"{min_date.date()} to {max_date.date()}"

    report = f"""# Data Quality Report

## Dataset Overview

| Check | Value |
|---|---:|
| Rows | {len(data):,} |
| Columns | {len(data.columns):,} |
| Numeric / boolean columns | {numeric_count:,} |
| Categorical columns | {categorical_count:,} |
| Duplicate order IDs | {duplicate_order_ids:,} |
| Bad review count | {target_count:,} |
| Bad review rate | {format_percent(target_rate)} |
| Order date range | {date_section} |

## Target Definition

```text
bad_review = 1 if review_score <= 2 else 0
```

This target is imbalanced, so PR-AUC, recall, precision, and threshold analysis are more useful than accuracy alone.

## Missing Values

{missing_section}

Full missing-value details:

```text
reports/data_quality_missing_values.csv
```

## Data Quality Interpretation

- The dataset is large enough for supervised machine learning experiments.
- The target is imbalanced, which makes random accuracy misleading.
- `order_id` uniqueness is checked because duplicate IDs could distort evaluation.
- Missing values are handled inside the modeling pipeline with median imputation for numeric features and most-frequent imputation for categorical features.
- Time-based validation is included separately to check whether the model generalizes to later orders.
"""
    DATA_QUALITY_REPORT.write_text(report, encoding="utf-8")
    print(f"Saved data quality report to {DATA_QUALITY_REPORT}")
    print(f"Saved missing-value table to {DATA_QUALITY_MISSING_VALUES}")


if __name__ == "__main__":
    main()
