# Advanced Modeling Results

## What Was Improved

This stage added four meaningful improvements:

1. Leakage-aware historical risk features.
2. Separate pre-delivery and post-delivery prediction modes.
3. Optuna tuning for LightGBM, XGBoost, and CatBoost.
4. Probability calibration for the best model.

## Why These Improvements Matter

The previous model answered:

```text
Can we predict bad customer experience from order data?
```

The advanced stage asks more realistic ML questions:

```text
Can we predict risk before delivery?
How much do delivery outcome features improve performance?
Which model family works best after tuning?
Are the predicted probabilities reliable enough for threshold decisions?
```

## Prediction Modes

### Pre-Delivery Model

Uses features available before delivery outcome is known. This is the more realistic early-warning model.

Excluded features:

- `delivery_time_days`
- `delivery_delay_days`
- `is_late`

### Post-Delivery Model

Uses delivery outcome features. This model is useful after delivery but before the customer submits a review.

This mode performs better because late delivery and delivery duration are strong signals of poor experience.

## Best Advanced Model

The best overall model was:

```text
Post-delivery LightGBM
```

Best test performance:

| Metric | Value |
|---|---:|
| Accuracy | 0.8413 |
| Precision | 0.4683 |
| Recall | 0.5905 |
| F1 | 0.5223 |
| ROC-AUC | 0.7948 |
| PR-AUC | 0.5570 |
| Brier score | 0.1420 |

Compared with the previous tuned LightGBM, the advanced model improved:

- PR-AUC: `0.5508` to `0.5570`
- ROC-AUC: `0.7875` to `0.7948`
- Recall: `0.5836` to `0.5905`
- F1: `0.5188` to `0.5223`

The improvement is modest but meaningful because it came from cleaner feature engineering and more realistic experiment design.

## Pre-Delivery vs Post-Delivery

Best pre-delivery model:

```text
LightGBM
```

Best pre-delivery test PR-AUC:

```text
0.4186
```

Best post-delivery test PR-AUC:

```text
0.5570
```

Interpretation:

The model can predict some risk before delivery, but delivery outcome information substantially improves prediction. This is a useful business finding: operational delivery performance is one of the strongest predictors of poor customer experience.

## Model Family Comparison

Post-delivery test PR-AUC:

| Model | PR-AUC | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| LightGBM | 0.5570 | 0.4683 | 0.5905 | 0.5223 |
| XGBoost | 0.5561 | 0.4938 | 0.5778 | 0.5325 |
| CatBoost | 0.5472 | 0.4810 | 0.5809 | 0.5262 |

Interpretation:

LightGBM had the best PR-AUC, while XGBoost had the strongest F1 in this run. This means LightGBM ranks risky orders slightly better overall, but XGBoost may be competitive if the business optimizes for default-threshold F1.

## Threshold Findings

For the best LightGBM model:

| Threshold | Flagged Order Rate | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.40 | 0.2826 | 0.3502 | 0.6737 | 0.4608 |
| 0.50 | 0.1853 | 0.4683 | 0.5905 | 0.5223 |
| 0.60 | 0.1341 | 0.5801 | 0.5295 | 0.5537 |
| 0.70 | 0.1048 | 0.6659 | 0.4750 | 0.5545 |
| 0.80 | 0.0861 | 0.7245 | 0.4246 | 0.5355 |

Business interpretation:

- If the team wants to catch more risky orders, use threshold `0.40`.
- If the team wants a balanced operating point, use threshold `0.60`.
- If the team wants high precision and fewer false alerts, use threshold `0.70` or `0.80`.

## Calibration

Calibration improved probability reliability:

| Metric | Raw | Calibrated |
|---|---:|---:|
| Brier score | 0.1420 | 0.0890 |
| PR-AUC | 0.5570 | 0.5462 |

Interpretation:

Calibration made probability estimates much more reliable, although it slightly reduced ranking performance. This is a common tradeoff:

- use raw scores when ranking orders by risk
- use calibrated scores when communicating probability estimates

## Final Business Interpretation

The strongest model is useful as an order-risk ranking system. It can help an e-commerce operations team decide which orders should receive attention first.

The project now shows:

- classical ML baselines
- tuned gradient boosting models
- CatBoost comparison
- leakage-aware historical features
- pre-delivery vs post-delivery modeling
- threshold tuning
- probability calibration
- business interpretation of precision/recall tradeoffs

## Explainability And Error Analysis

Additional outputs:

```text
reports/shap_feature_importance.csv
reports/error_analysis/error_summary.csv
reports/error_analysis/true_positive_examples.csv
reports/error_analysis/false_positive_examples.csv
reports/error_analysis/false_negative_examples.csv
```

Top SHAP features:

| Feature | Interpretation |
|---|---|
| `delivery_delay_days` | Late delivery strongly increases risk. |
| `seller_prior_bad_review_rate` | Historical seller quality is predictive. |
| `delivery_time_days` | Longer delivery duration affects customer experience. |
| `order_item_count` | More complex orders carry different risk. |
| `category_prior_bad_review_rate` | Some product categories have higher historical risk. |

Error analysis at threshold `0.60`:

| Error Type | Orders | Avg Risk Score | Avg Delay Days | Avg Delivery Time |
|---|---:|---:|---:|---:|
| True positive | 1,535 | 0.887 | 5.185 | 30.440 |
| False positive | 1,111 | 0.775 | -3.836 | 22.061 |
| False negative | 1,364 | 0.336 | -12.687 | 12.041 |
| True negative | 15,725 | 0.283 | -12.727 | 10.755 |

Interpretation:

The model is especially strong at identifying late, slow, operationally risky orders. False negatives often look operationally normal from available features, which suggests future improvements should add support-ticket text, seller response behavior, or product/customer feedback signals if available.
