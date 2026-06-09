# Model Card: E-Commerce Bad Review Risk Model

## Model Overview

This model predicts whether an e-commerce order is at risk of producing a poor customer experience.

Target:

```text
bad_review = 1 if review_score <= 2 else 0
```

Final champion model:

```text
CV-tuned post-delivery LightGBM
```

Model artifact:

```text
models/cv_tuned_lightgbm_model.joblib
```

## Intended Use

The model is intended as a decision-support tool for ranking orders by customer experience risk.

Possible business uses:

- prioritize high-risk orders for support review
- identify seller, category, and delivery patterns linked to poor experience
- support proactive customer follow-up
- guide operational investigation into delayed or complex orders

The model should be used to assist human teams, not to automatically penalize customers or sellers.

## Not Intended For

The model should not be used for:

- automatic seller punishment
- customer eligibility decisions
- financial credit decisions
- fully automated refunds or cancellations
- decisions without human review

## Dataset

Dataset:

```text
Olist Brazilian E-Commerce public dataset
```

Current modeling dataset:

```text
Rows: 98,673
Columns: 49
Bad review rate: 14.69%
Date range: 2016-09-04 to 2018-10-17
```

Feature groups:

- order status and order complexity
- product category and product attributes
- payment value and payment type
- seller and customer geography
- delivery timing and delay features
- historical seller/category/location prior-risk features

## Performance

Random baseline PR-AUC is approximately the bad-review rate:

```text
Random PR-AUC baseline: ~0.1469
```

Final random-split test result:

```text
PR-AUC:    0.5612
ROC-AUC:   0.7964
Precision: 0.4681
Recall:    0.5992
F1:        0.5256
```

This is approximately 3.8x above the random PR-AUC baseline.

Future-period validation:

```text
Best future-period test PR-AUC: 0.4148
```

The time-based score is lower, which indicates that future deployment is harder than random-split evaluation. This should be treated as an important realism check.

## Threshold Recommendation

Current cost-assumption threshold:

```text
Recommended threshold: 0.50
Flagged order rate:   18.80%
Precision:            0.4681
Recall:               0.5992
```

If support capacity is limited, a higher threshold such as `0.60` can reduce the number of flagged orders while increasing precision.

## Precision-Focused Modes

For teams with limited review capacity, the model can be operated in high-precision mode.

Held-out test examples:

```text
High-confidence threshold: precision 0.8188, recall 0.2556, flagged 4.59%
Top-5% review policy:      precision 0.8131, recall 0.2822, flagged 5.10%
```

These policies are not replacements for the balanced model. They are operating modes for situations where false positives are expensive or support capacity is limited.

Separate challenger models were also trained:

```text
models/precision_focused_lightgbm_model.joblib
models/critical_risk_lightgbm_model.joblib
```

## Explainability

Important risk drivers from SHAP and feature analysis include:

- delivery delay
- delivery time
- seller prior bad-review rate
- seller prior late-delivery rate
- category prior bad-review rate
- order item count
- product size and complexity

These drivers align with the business interpretation that poor customer experience is linked to operational delay, seller reliability, category risk, and order complexity.

## Limitations

- The dataset is historical and public, not live company data.
- The model does not include support tickets, customer messages, refund logs, carrier events, or complaint text.
- Post-delivery features are highly predictive but are not available for early intervention before delivery.
- Time-based validation shows that performance drops on later orders.
- Cost assumptions are placeholders and should be replaced with real company economics.

## Monitoring Recommendations

If deployed, monitor:

- PR-AUC and recall over time
- bad-review rate over time
- predicted risk score distribution
- feature drift by seller, category, and location
- precision and recall at the chosen business threshold
- calibration drift
- false positive and false negative examples

## Retraining Recommendation

Retrain monthly or when:

- bad-review rate changes meaningfully
- delivery operations change
- new sellers/categories are added
- model PR-AUC or recall drops below an agreed threshold
- risk score distribution shifts from historical levels
