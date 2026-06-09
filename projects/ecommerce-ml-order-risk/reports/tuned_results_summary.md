# Tuned Model Results

## Objective

Tune the strongest baseline model families and choose a practical model for predicting poor customer experience in e-commerce orders.

Target:

```text
bad_review = 1 if review_score <= 2 else 0
```

## Tuned Model Families

The tuning stage focused on:

- Random Forest
- XGBoost
- LightGBM

These were chosen because they performed strongest in the baseline stage and are well-suited to tabular business data.

## Best Model

The best validation model was:

```text
LightGBM
```

Best parameters:

```text
learning_rate = 0.04
min_child_samples = 60
n_estimators = 350
num_leaves = 31
```

## Test Set Performance

| Metric | Value |
|---|---:|
| Accuracy | 0.8409 |
| Precision | 0.4669 |
| Recall | 0.5836 |
| F1 | 0.5188 |
| ROC-AUC | 0.7875 |
| PR-AUC | 0.5508 |

Confusion matrix at threshold `0.50`:

| Result | Count |
|---|---:|
| True negatives | 14,904 |
| False positives | 1,932 |
| False negatives | 1,207 |
| True positives | 1,692 |

## Threshold Interpretation

The default threshold of `0.50` is not necessarily the best business threshold.

Examples:

| Threshold | Flagged Order Rate | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.35 | 0.3633 | 0.2874 | 0.7109 | 0.4094 |
| 0.40 | 0.2784 | 0.3467 | 0.6571 | 0.4539 |
| 0.50 | 0.1836 | 0.4669 | 0.5836 | 0.5188 |
| 0.60 | 0.1327 | 0.5710 | 0.5157 | 0.5420 |
| 0.70 | 0.1018 | 0.6706 | 0.4650 | 0.5492 |

Business interpretation:

- Lower thresholds catch more bad-review orders but create more false alarms.
- Higher thresholds flag fewer orders but make each flag more reliable.
- If customer support capacity is limited, a threshold around `0.60` or `0.70` may be more practical.
- If preventing bad reviews is more important than support workload, a threshold around `0.35` or `0.40` may be better.

## Top Drivers

Top feature importance signals include:

- delivery delay days
- delivery time days
- product description length
- approval time hours
- product volume
- total freight
- product weight
- estimated delivery days
- freight ratio
- payment value

Interpretation:

The model is learning a realistic business pattern: customer experience risk is strongly connected to delivery performance, freight/product characteristics, order value, and operational timing.

## Why This Matters

This model could support an e-commerce operations team by ranking orders for proactive intervention.

Possible business actions:

- check late or delayed orders
- prioritize support outreach for high-risk orders
- investigate sellers/products linked to poor experience
- monitor freight-heavy or difficult-to-deliver products
- tune intervention thresholds based on support capacity

## Current Limitations

- The model predicts risk from historical order data, not live real-time events.
- The dataset is anonymized and does not include every possible customer-support signal.
- Some features may only be available after delivery, so future iterations should separate pre-delivery and post-delivery prediction modes.
- Threshold choice should be based on business cost, support capacity, and acceptable false alarm rate.

## Next Steps

- Add SHAP explainability for individual predictions.
- Build false positive and false negative error analysis.
- Create a pre-delivery-only feature set.
- Compare final model performance against a simple rule-based baseline.
- Save a final case-study notebook or report.

