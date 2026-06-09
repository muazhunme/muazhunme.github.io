# Case Study: E-Commerce Bad Review Risk Prediction

## Problem

E-commerce teams often learn about a customer problem only after the customer leaves a poor review. By then, the customer may already be frustrated and the business has limited time to recover the experience.

This project asks:

```text
Can we predict which orders are most likely to create a poor customer experience?
```

The target was defined as:

```text
bad_review = 1 if review_score <= 2 else 0
```

## Data

The project uses the Olist Brazilian E-Commerce public dataset. It contains structured business tables for:

- orders
- customers
- sellers
- products
- order items
- payments
- reviews

These tables were joined into one order-level modeling dataset.

Final modeling dataset:

```text
Rows: 98,673
Columns: 49
Bad review rate: 14.69%
Date range: 2016-09-04 to 2018-10-17
```

## What Was Built

The project turns raw relational-style tables into a machine learning decision-support system.

Main work completed:

- joined multiple business tables into an order-level dataset
- handled missing values and duplicate checks
- engineered delivery, seller, category, payment, location, and order-complexity features
- trained and compared multiple model families
- tuned the strongest models with cross-validation
- checked overfitting with learning curves and time-based validation
- added explainability, threshold analysis, risk bands, and recommended support actions

## Model

Champion model:

```text
CV-tuned post-delivery LightGBM
```

Final random-split test performance:

```text
PR-AUC:    0.5612
ROC-AUC:   0.7964
Precision: 0.4681
Recall:    0.5992
F1:        0.5256
```

Because bad reviews are only 14.69% of orders, the random PR-AUC baseline is approximately 0.1469. The final PR-AUC is about 3.8x higher than random ranking.

## Business Use

The model can rank orders by risk so a support team can prioritize where to intervene.

Example operating modes:

```text
Balanced mode:       threshold 0.50, broader coverage
High-precision mode: top 5-10% highest-risk orders
Critical-risk mode:  separate one-star risk model
```

Best high-precision test result:

```text
Threshold:  0.9394
Precision: 0.8188
Recall:    0.2556
Flagged:   4.59% of orders
```

This is useful when a support team has limited capacity and wants fewer false positives.

## Explainability

The strongest risk signals included:

- delivery delay
- delivery time
- seller prior bad-review rate
- seller prior late-delivery rate
- category prior bad-review rate
- order item count

This creates a clear business story: poor customer experience is strongly connected to operational delay, seller reliability, category risk, and order complexity.

## Limitations

- The dataset is public and historical, not live company data.
- Post-delivery features are powerful but not always available before intervention.
- The model does not include support tickets, refund logs, complaint text, or carrier tracking events.
- Time-based validation was harder than random-split validation, so future deployment would need monitoring.
- Cost assumptions are placeholders and should be replaced with real company economics.

## Final Outcome

This project is not just a model comparison notebook. It is a portfolio-ready ML case study showing:

- data preparation from relational-style tables
- practical feature engineering
- model comparison and tuning
- overfitting checks
- explainability
- threshold strategy
- business-facing risk scoring
- production-style documentation
