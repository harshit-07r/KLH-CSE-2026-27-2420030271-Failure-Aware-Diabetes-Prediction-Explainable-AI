# Research Reproducibility and Audit Checklist

| Item | Requirement | Verification Standard | Project Audit Verdict | Evidence File |
|:---:|:---|:---|:---:|:---|
| **R-01** | Python Version | >= 3.10 | **VERIFIED** (Python 3.12 / 3.10 compatible) | `requirements.txt` |
| **R-02** | Random Seed Protocol | Deterministic seed = 42 across all splits & CV | **VERIFIED** | `src/config.py`, Notebook 02 |
| **R-03** | Train/Test Split | Stratified 80/20 partition ($N_{train}=202,944, N_{test}=50,736$) | **VERIFIED** | `data/CLASS_DISTRIBUTION.csv` |
| **R-04** | Missing Value Handling | 0 missing values; zero imputation leakage | **VERIFIED** | `data/DATA_QUALITY_REPORT.csv` |
| **R-05** | Scaler Fitting | Fitted strictly on training folds; test transformed out-of-sample | **VERIFIED** | `src/data_processing/preprocess.py` |
| **R-06** | OOF Meta-Feature Protocol | Meta-learner trained strictly on CV out-of-fold probability slices | **VERIFIED** | `src/models/oof_generator.py` |
| **R-07** | Locked Test Isolation | Zero test instances queried during feature selection or meta-training | **VERIFIED** | `reports/audit/leakage_audit.md` |
| **R-08** | Statistical Significance | Paired bootstrap (B=1,000) & McNemar test ($p < 1e-27$) | **VERIFIED** | `results/final/statistical_comparisons.csv` |
| **R-09** | Duplicate Record Audit | 23,899 corpus duplicates; 6,923 test overlap documented | **VERIFIED** | `results/final/duplicate_profile_comparison.csv` |
| **R-10** | Explainability Lineage | SHAP TreeExplainer on XGBoost; LIME on Patient 134330 | **VERIFIED** | `reports/validation/explainability_audit.md` |
| **R-11** | Public Health Surveillance | CDC USDSS 2000-2024 demarcated from ML testing | **VERIFIED** | `reports/POPULATION_SURVEILLANCE_ANALYSIS.md` |
