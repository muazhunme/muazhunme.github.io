# Overfitting and Fine-Tuning Summary

## Goal

The goal of this stage was to improve the model without simply making it more complex. The work focused on three questions:

- Does the model generalize beyond the training data?
- Does performance hold up when tested on future orders?
- Can hyperparameter tuning improve PR-AUC while using regularization to control overfitting?

## Methods Used

### 1. Time-Based Validation

The data was sorted by `order_purchase_timestamp` and split into:

- first 60% of orders for training
- next 20% for validation
- final 20% for future-period testing

This is stricter than a random split because it tests whether the model can handle later customer behavior and operational patterns.

Best future-period test result:

```text
XGBoost test PR-AUC: 0.4148
LightGBM test PR-AUC: 0.4084
CatBoost test PR-AUC: 0.4040
```

This showed that the random-split score is optimistic. The model still learns useful patterns, but future-period prediction is harder and should be reported separately.

### 2. Learning Curve

The LightGBM learning curve showed that more training data reduced the overfitting gap:

```text
10% training data:  train PR-AUC 0.9262, holdout PR-AUC 0.5142, gap 0.4120
100% training data: train PR-AUC 0.6613, holdout PR-AUC 0.5597, gap 0.1015
```

This is a positive sign. The model is not only memorizing; it becomes more stable as more data is used.

### 3. Cross-Validated LightGBM Tuning

Optuna was used with 4-fold stratified cross-validation to tune LightGBM. The search included regularization and complexity controls:

- lower learning rate
- tree depth limit
- minimum child samples
- row and column subsampling
- L1 and L2 regularization
- minimum split gain

Best cross-validated LightGBM result:

```text
Mean CV PR-AUC: 0.5698
Test PR-AUC:    0.5612
ROC-AUC:        0.7964
Precision:      0.4681
Recall:         0.5992
F1:             0.5256
```

This improved the previous best post-delivery LightGBM PR-AUC:

```text
Previous PR-AUC: 0.5570
CV-tuned PR-AUC: 0.5612
```

## Final Interpretation

The best final model is the CV-tuned LightGBM model. It gives the strongest random-split performance while using regularized hyperparameters and cross-validation.

The time-based validation result should also be kept in the project because it makes the case study more realistic. It shows that the model is useful, but future-period performance is harder than random-split performance.

## Final Model Artifact

```text
models/cv_tuned_lightgbm_model.joblib
```

## Supporting Files

```text
reports/cv_tuning_results.csv
reports/time_validation_results.csv
reports/learning_curve_results.csv
reports/learning_curve.png
reports/time_validation_pr_auc.png
```
