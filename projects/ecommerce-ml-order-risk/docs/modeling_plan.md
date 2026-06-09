# Modeling Plan

## 1. Problem Definition

Predict whether an e-commerce order will lead to a poor customer experience.

Target:

```text
bad_review = review_score <= 2
```

This is a binary classification problem with class imbalance.

## 2. Why This Problem Matters

A business could use this model to:

- flag risky orders before negative reviews accumulate
- prioritize customer support outreach
- investigate delivery delays
- identify seller or product categories linked to poor experience
- reduce customer churn and reputation damage

## 3. Data Preparation

Current dataset creation steps:

- Load raw Olist tables.
- Join orders with reviews, items, payments, products, sellers, and customers.
- Aggregate item-level and payment-level data to order level.
- Engineer delivery, timing, payment, freight, product, location, and historical prior-risk features.
- Save clean modeling datasets for post-delivery, pre-delivery, and temporal validation experiments.

## 4. Baseline Models

The first baseline compares:

- linear model: Logistic Regression
- tree model: Decision Tree
- ensemble model: Random Forest
- distance-based model: KNN
- margin-based model: Linear SVM
- probabilistic model: Naive Bayes
- boosting models: Gradient Boosting, XGBoost, LightGBM

This gives broad algorithm coverage and shows how different model families behave on the same business problem.

## 5. Evaluation Metrics

Accuracy is not enough because bad reviews are the minority class.

Primary metrics:

- PR-AUC
- Recall
- Precision
- F1

Supporting metrics:

- ROC-AUC
- Brier score
- Confusion matrix

Business interpretation:

- Higher recall means catching more risky orders.
- Higher precision means fewer unnecessary interventions.
- Threshold tuning decides the business tradeoff.
- Calibration checks whether predicted risk scores are reliable probabilities.

## 6. Tuning and Advanced Experiments

Completed tuning and advanced modeling:

- LightGBM, XGBoost, and Random Forest tuning
- Optuna tuning
- CatBoost comparison
- leakage-aware prior-risk features
- pre-delivery vs post-delivery datasets
- probability calibration
- SHAP feature importance
- error analysis examples

Strongest advanced model before cross-validation:

```text
Post-delivery LightGBM
```

Key result:

```text
PR-AUC improved from 0.5508 to 0.5570
ROC-AUC improved from 0.7875 to 0.7948
```

The pre-delivery model performs worse than the post-delivery model, which is expected and useful. It shows that delivery outcome features contain strong information about poor customer experience risk.

## 7. Overfitting Control and Final Tuning

Completed safeguards:

- chronological train/validation/test split
- learning curve analysis
- 4-fold stratified cross-validated LightGBM tuning
- regularization-focused hyperparameter search

Time-based validation result:

```text
Best future-period test PR-AUC: 0.4148
```

Learning curve result:

```text
Generalization gap reduced from 0.4120 to 0.1015 as the full training data was used.
```

Best final model:

```text
CV-tuned post-delivery LightGBM
```

Final random-split test result:

```text
PR-AUC:    0.5612
ROC-AUC:   0.7964
Precision: 0.4681
Recall:    0.5992
F1:        0.5256
```

The time-based result should be reported beside the random-split result because it gives a more realistic estimate of future deployment difficulty.

## 8. Current Saved Outputs

- `reports/baseline_model_results.csv`
- `reports/baseline_results_summary.md`
- `reports/tuned_model_results.csv`
- `reports/tuned_results_summary.md`
- `reports/threshold_analysis.csv`
- `reports/feature_importance.csv`
- `reports/advanced_model_results.csv`
- `reports/advanced_results_summary.md`
- `reports/advanced_threshold_analysis.csv`
- `reports/calibration_results.csv`
- `reports/shap_feature_importance.csv`
- `reports/error_analysis/error_summary.csv`
- `reports/time_validation_results.csv`
- `reports/learning_curve_results.csv`
- `reports/cv_tuning_results.csv`
- `reports/overfitting_validation_summary.md`
- `reports/data_quality_report.md`
- `reports/business_threshold_analysis.csv`
- `reports/business_threshold_summary.md`
- `reports/scored_orders.csv`
- `reports/high_risk_orders_sample.csv`
- `reports/MODEL_CARD.md`
- `reports/precision_policy_results.csv`
- `reports/precision_policy_summary.md`
- `reports/learning_curve.png`
- `reports/time_validation_pr_auc.png`
- `reports/business_threshold_tradeoff.png`
- `reports/precision_policy_tradeoff.png`
- `models/best_order_risk_model.joblib`
- `models/advanced_best_order_risk_model.joblib`
- `models/cv_tuned_lightgbm_model.joblib`

## 9. Final Deliverable

The final project should include:

- clean README
- reproducible scripts
- documented dataset construction
- model comparison
- tuned best model
- overfitting validation
- data quality report
- cost-based threshold recommendation
- precision-focused operating policies
- scored high-risk order sample
- model card
- business interpretation
- explainability section
- final recommendation
