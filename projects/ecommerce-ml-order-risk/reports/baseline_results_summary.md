# Baseline Model Results

Dataset:

- Rows: 98,673 orders
- Target: `bad_review = 1` when `review_score <= 2`
- Bad review rate: 14.69%

## Current Ranking

The strongest first-pass models are:

| Rank | Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | LightGBM | 0.8388 | 0.4615 | 0.5847 | 0.5158 | 0.7894 | 0.5542 |
| 2 | Gradient Boosting | 0.8917 | 0.7402 | 0.4050 | 0.5235 | 0.7837 | 0.5538 |
| 3 | XGBoost | 0.8373 | 0.4581 | 0.5861 | 0.5142 | 0.7889 | 0.5513 |
| 4 | Random Forest | 0.8536 | 0.5016 | 0.5492 | 0.5243 | 0.7871 | 0.5296 |
| 5 | Decision Tree | 0.8436 | 0.4731 | 0.5692 | 0.5167 | 0.7710 | 0.5225 |

## Early Interpretation

LightGBM, XGBoost, and Random Forest are the most promising models for this problem because they balance recall and precision better than the simpler baselines.

For this business problem, recall matters because missed bad-review orders are missed chances to intervene. Precision also matters because a business does not want to over-escalate too many normal orders. The next stage should tune the classification threshold and compare models based on business cost, not just default 0.5 predictions.

## Next Steps

- Tune LightGBM, XGBoost, and Random Forest with cross-validation.
- Compare thresholds for high-recall versus balanced precision/recall strategies.
- Add confusion matrices and precision-recall curves.
- Run feature importance and SHAP explanations.
- Add error analysis: false positives and false negatives.
- Save the best model pipeline in `models/`.

