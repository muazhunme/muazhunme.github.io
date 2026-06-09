# E-Commerce Order Risk Prediction

Machine learning case study that predicts which e-commerce orders are most likely to lead to a poor customer experience.

The project uses the Olist Brazilian E-Commerce dataset and turns multiple relational-style tables into an order-level risk prediction system.

## What I Built

- Joined orders, customers, sellers, products, payments, reviews, and order items into one modeling dataset.
- Engineered features around delivery delay, seller reliability, category risk, payment patterns, freight ratio, and order complexity.
- Compared baseline models, then tuned LightGBM, XGBoost, CatBoost, and other candidates.
- Added overfitting checks with learning curves and time-based validation.
- Built business-facing outputs: risk bands, threshold analysis, high-risk order samples, model card, and support recommendations.
- Added a static frontend demo for non-technical viewers.

## Dataset

```text
Rows: 98,673
Columns: 49
Bad review rate: 14.69%
Target: bad_review = 1 if review_score <= 2
```

Raw/processed datasets and saved model files are excluded from GitHub because they are large generated artifacts.

## Final Model

Champion model:

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

Because bad reviews are only 14.69% of orders, the random PR-AUC baseline is about 0.1469. The final model is roughly 3.8x better than random ranking.

## High-Precision Mode

For support teams with limited capacity, I added high-confidence operating policies.

```text
Top-5% review policy precision: 0.8131
Top-5% review policy recall:    0.2822
Flagged order rate:             5.10%
```

## Key Files

```text
src/                         Reproducible Python scripts
docs/case_study.md           Short business case study
reports/MODEL_CARD.md        Model card and limitations
reports/*.csv                Result tables
reports/*.png                Analysis charts
portfolio_demo/index.html    Static frontend demo
```

## Run Locally

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Regenerate the main artifacts using the existing champion model:

```powershell
python src/run_full_pipeline.py
```

Rerun cross-validated model tuning:

```powershell
python src/run_full_pipeline.py --retrain
```

Open the frontend demo:

```powershell
cd portfolio_demo
python -m http.server 8080
```

Then visit:

```text
http://localhost:8080
```

## Portfolio Summary

This project shows practical machine learning beyond model training: data preparation, feature engineering, model comparison, cross-validation, overfitting checks, explainability, threshold strategy, and business-facing risk scoring.
