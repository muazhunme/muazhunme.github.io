# Project Structure

```text
ecommerce-ml-order-risk/
|-- data/
|   |-- raw/                  # Original Olist CSV files
|   `-- processed/            # ML-ready datasets created from raw files
|-- docs/                     # Human-readable project documentation
|-- models/                   # Saved trained model pipelines
|-- notebooks/                # Optional notebooks for exploration
|-- reports/                  # Model results, summaries, plots, and analysis notes
|-- portfolio_demo/           # Static non-technical project demo
|-- src/                      # Reproducible Python scripts
|-- README.md                 # Main project overview
`-- requirements.txt          # Python dependencies
```

## Important Files

`src/make_dataset.py`

Builds the modeling table by joining raw Olist tables and engineering features for customer experience risk prediction.

`src/train_baselines.py`

Runs the first model comparison across classical ML and boosting algorithms.

`src/tune_models.py`

Runs controlled tuning for the strongest model families.

`src/advanced_experiments.py`

Runs Optuna, CatBoost comparison, calibration, and pre-delivery vs post-delivery experiments.

`src/explain_model.py`

Creates SHAP feature importance and false positive / false negative examples.

`src/time_validation.py`

Tests model performance on future-period orders using a chronological split.

`src/learning_curves.py`

Measures how the training and holdout PR-AUC gap changes as more data is used.

`src/cv_tune_lightgbm.py`

Runs cross-validated LightGBM tuning with regularization-focused hyperparameters.

`src/data_quality_report.py`

Creates a data quality report covering row counts, column counts, missing values, target rate, duplicates, and date range.

`src/business_threshold_analysis.py`

Converts model thresholds into a cost-based business decision table.

`src/score_orders.py`

Scores orders, assigns risk bands, adds top risk reasons, and recommends support actions.

`src/run_full_pipeline.py`

Runs the full reproducible project pipeline from dataset creation through scoring artifacts.

`src/precision_policy_experiments.py`

Tests high-precision thresholds, top-k review policies, a precision-focused challenger model, and a critical one-star risk model.

`data/processed/order_risk_modeling.csv`

The main ML-ready dataset used by training scripts.

`reports/baseline_model_results.csv`

Model comparison metrics from the baseline training run.

`reports/baseline_results_summary.md`

Short written interpretation of current baseline results.

`reports/overfitting_validation_summary.md`

Written interpretation of time validation, learning curves, and cross-validated tuning.

`reports/MODEL_CARD.md`

Production-style model documentation covering intended use, limitations, metrics, monitoring, and retraining.

`reports/precision_policy_summary.md`

Summarizes high-precision operating modes and their held-out test precision/recall tradeoffs.

`docs/case_study.md`

Concise portfolio case study covering problem, data, model, result, business use, and limitations.

`portfolio_demo/index.html`

Static frontend demo for explaining the project to non-technical viewers.

## Organization Rules

- Raw data stays in `data/raw/`.
- Processed datasets stay in `data/processed/`.
- Repeatable code goes in `src/`.
- Notes and explanations go in `docs/`.
- Model outputs and result files go in `reports/` or `models/`.
- Avoid mixing notebooks, raw data, and final outputs in the same folder.
