# Data Quality Report

## Dataset Overview

| Check | Value |
|---|---:|
| Rows | 98,673 |
| Columns | 49 |
| Numeric / boolean columns | 42 |
| Categorical columns | 7 |
| Duplicate order IDs | 0 |
| Bad review count | 14,493 |
| Bad review rate | 14.69% |
| Order date range | 2016-09-04 to 2018-10-17 |

## Target Definition

```text
bad_review = 1 if review_score <= 2 else 0
```

This target is imbalanced, so PR-AUC, recall, precision, and threshold analysis are more useful than accuracy alone.

## Missing Values

| Column | Missing Count | Missing Rate |
|---|---:|---:|
| seller_prior_avg_delay_days | 3,084 | 3.13% |
| seller_prior_bad_review_rate | 3,084 | 3.13% |
| seller_prior_late_rate | 3,084 | 3.13% |
| delivery_delay_days | 2,843 | 2.88% |
| delivery_time_days | 2,843 | 2.88% |
| product_category | 2,161 | 2.19% |
| product_description_lenght | 2,161 | 2.19% |
| product_name_lenght | 2,161 | 2.19% |
| product_photos_qty | 2,161 | 2.19% |
| product_volume_cm3 | 772 | 0.78% |
| product_weight_g | 772 | 0.78% |
| avg_price | 756 | 0.77% |
| freight_ratio | 756 | 0.77% |
| order_item_count | 756 | 0.77% |
| product_count | 756 | 0.77% |

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
