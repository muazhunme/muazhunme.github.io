# Business Threshold Summary

## Cost Assumptions

These are simple placeholder assumptions used to make threshold selection business-oriented:

```text
Missed bad review cost:              100
Unnecessary support intervention:    10
Successful intervention savings:     60
```

The purpose is not to claim exact financial value. The purpose is to show how a company would connect model thresholds to operational cost.

## Recommended Threshold

```text
Threshold:                    0.50
Flagged order rate:            18.80%
Precision:                     0.4681
Recall:                        0.5992
Estimated savings vs no model: 84480
```

## Interpretation

This threshold is the best option under the current cost assumptions. If support capacity is limited, the business may choose a higher threshold to review fewer orders with higher precision. If customer retention is the priority, the business may choose a lower threshold to catch more risky orders.

Full threshold table:

```text
reports/business_threshold_analysis.csv
```
