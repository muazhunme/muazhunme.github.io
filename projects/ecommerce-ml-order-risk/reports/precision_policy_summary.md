# Precision Policy Summary

## Purpose

This experiment tested ways to increase precision without replacing the champion model blindly.

Safeguards used:

- thresholds were selected on validation data
- final results were measured on held-out test data
- the original champion model remains unchanged
- precision-focused and critical-risk models are treated as challenger policies

## Best High-Precision Bad-Review Policies

                        model                                             policy  test_threshold  test_flagged_order_rate  test_precision  test_recall  test_true_positives  test_false_positives
   champion_balanced_lightgbm max_precision_with_validation_recall_at_least_0.25        0.939420                 0.045858        0.818785     0.255605                741.0                 164.0
   champion_balanced_lightgbm                review_top_5pct_highest_risk_orders        0.934296                 0.050975        0.813121     0.282166                818.0                 188.0
unweighted_precision_lightgbm max_precision_with_validation_recall_at_least_0.25        0.744020                 0.047074        0.810549     0.259745                753.0                 176.0
unweighted_precision_lightgbm                review_top_5pct_highest_risk_orders        0.723776                 0.051786        0.807241     0.284581                825.0                 197.0
  precision_weighted_lightgbm max_precision_with_validation_recall_at_least_0.25        0.846530                 0.047175        0.804511     0.258365                749.0                 182.0

## Best Bad-Review Policies With At Least 35% Test Recall

                        model                                             policy  test_threshold  test_flagged_order_rate  test_precision  test_recall  test_true_positives  test_false_positives
   champion_balanced_lightgbm max_precision_with_validation_recall_at_least_0.35        0.905000                 0.066633        0.784030     0.355640               1031.0                 284.0
unweighted_precision_lightgbm max_precision_with_validation_recall_at_least_0.45        0.360940                 0.094857        0.692308     0.447051               1296.0                 576.0
  precision_weighted_lightgbm max_precision_with_validation_recall_at_least_0.45        0.505000                 0.095769        0.689947     0.449810               1304.0                 586.0
   champion_balanced_lightgbm max_precision_with_validation_recall_at_least_0.45        0.730000                 0.096428        0.686285     0.450500               1306.0                 597.0
   champion_balanced_lightgbm               review_top_10pct_highest_risk_orders        0.705238                 0.101039        0.671515     0.461883               1339.0                 655.0

## Critical One-Star Risk Model

                     model                                             policy  test_threshold  test_flagged_order_rate  test_precision  test_recall  test_true_positives  test_false_positives
critical_one_star_lightgbm max_precision_with_validation_recall_at_least_0.25        0.931140                 0.042564        0.746429     0.279039                627.0                 213.0
critical_one_star_lightgbm                review_top_5pct_highest_risk_orders        0.922253                 0.051482        0.724409     0.327548                736.0                 280.0
critical_one_star_lightgbm max_precision_with_validation_recall_at_least_0.35        0.915000                 0.057360        0.718198     0.361816                813.0                 319.0

## Interpretation

Precision can be increased by using stricter thresholds or top-k review policies. This reduces false positives and support workload, but it also lowers recall, meaning more bad-review orders are missed.

The production-style recommendation is to keep the CV-tuned LightGBM model as the champion ranking model and expose multiple operating modes:

```text
Balanced mode: use the existing 0.50 threshold.
High-precision mode: review only the top 5-10% highest-risk orders.
Critical-risk mode: use the separate one-star model for severe cases.
```

Full results:

```text
reports/precision_policy_results.csv
```
