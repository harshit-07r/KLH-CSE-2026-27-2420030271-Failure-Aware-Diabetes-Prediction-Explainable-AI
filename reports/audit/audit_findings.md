# Master Repository Audit Findings & Vulnerability Matrix

**Project Title:** Failure-Aware Hybrid Ensemble Learning With Explainable AI for Three-Class Diabetes Status Classification  
**Audit Standard:** Strict Peer Review, Mathematical Consistency, Empirical Reproducibility  
**Date:** 2026-10-29  

---

## 1. Executive Findings Summary

Every source file, model artifact, prediction file, and notebook in the repository was audited. The findings are categorized into a rigorous tracking matrix:

| Finding ID | Severity | Category | Affected File(s) | Description Summary | Status |
|:---:|:---:|:---:|:---|:---|:---:|
| **FND-01** | **CRITICAL** | Numerical Inconsistency | Notebook 12 vs Notebook 10 / Stacking Tables | Table 6 probabilities-only ablation reports Macro-F1 0.4199 / Prediabetes Recall 0.3402, whereas Table 2 Standard Stacking reports Macro-F1 0.4180 / Recall 0.4060. | **RECONCILED IN PHASE 2** |
| **FND-02** | **HIGH** | Estimator Misnomer | `models/base_models/svm.joblib`, Notebook 08 | Estimator labeled as "SVM" is actually `SGDClassifier(loss='modified_huber')`. True quadratic kernel SVM was not used. | **DOCUMENTED & RE-LABELED** |
| **FND-03** | **HIGH** | Architecture Divergence | `models/hybrid/` | Dual hybrid models exist: 50 meta-features (7 base models) vs 27 meta-features (5 base models, Pipeline wrapped). | **DOCUMENTED & SPECIFIED** |
| **FND-04** | **MEDIUM** | Duplicate Survey Vectors | `data/raw/`, `data/processed/` | 23,899 duplicate rows in full BRFSS 2015; 6,923 test rows share identical feature vectors with training instances due to discrete survey nature. | **AUDITED IN PHASE 4** |
| **FND-05** | **MEDIUM** | Statistical Reporting | Notebook 10, reports | Earlier text reported one-tailed bootstrap p = 0.076; two-tailed p = 0.224 for Macro-F1; McNemar p = 1.43e-28 for classification discordance. | **RECONCILED IN PHASE 5** |
| **FND-06** | **HIGH** | Minority Detection Reality | `TEST_PREDICTIONS_MASTER.csv` | Standard linear baselines detect only 4 prediabetes cases out of 926 (0.43% recall); Hybrid detects 360 cases (38.88% recall). | **VERIFIED IN PHASE 6** |
| **FND-07** | **MEDIUM** | Explainability Attribution | Notebook 13 | SHAP was computed using TreeExplainer on XGBoost rather than the full hybrid meta-learner; LIME Patient 134330 reveals socioeconomic masking. | **DOCUMENTED IN PHASE 7** |
| **FND-08** | **MEDIUM** | Secondary Dataset Role | `data/raw/export.csv`, Notebook 15 | CDC USDSS data (13,889 rows) is aggregate surveillance data (2000-2024), not individual-level test set validation. | **DEMARCATED IN PHASE 10** |

---

## 2. Detailed Findings and Remediation Directives

### Finding FND-01: Table 6 vs Table 2 Stacking Discrepancy (Critical)
- **Affected Artifacts:** `MANUSCRIPT_REWRITE_FILES/12_hybrid_ablation_results.csv`, `MANUSCRIPT_REWRITE_FILES/MODEL_COMPARISON_MASTER.csv`, Notebook 12.
- **Empirical Evidence:**
  - Table 6 (Ablation M1: Probabilities only) shows Accuracy = 0.6117, Macro-F1 = 0.4199, Prediabetes Recall = 0.3402.
  - Table 2 (Standard Stacking Corrected) shows Accuracy = 0.6000, Macro-F1 = 0.4180, Prediabetes Recall = 0.4060.
- **Root Cause:**
  - Table 6 M1 represents the *Original* Stacking baseline fitted prior to the balanced sample-weight correction.
  - Table 2 represents the *Corrected* Stacking baseline where inverse-frequency class weighting was applied to the OOF meta-learner.
- **Required Fix:** Recompute both configurations from raw OOF predictions on identical terms, document their provenance in `results/final/metrics_master.csv`, and present both in the manuscript with explicit labels.

### Finding FND-02: SVM Labeled Estimator is SGD with Modified Huber Loss (High)
- **Affected Artifacts:** `models/base_models/svm.joblib`, `notebooks/08_existing_models.ipynb`.
- **Empirical Evidence:** Inspecting `svm.joblib` shows `SGDClassifier(loss='modified_huber', penalty='l2', alpha=0.0001)`.
- **Scientific Impact:** Modified Huber loss is a smooth, linear convex surrogate with sigmoid-like probability estimation. True kernel SVM has $\mathcal{O}(N^2)$ to $\mathcal{O}(N^3)$ complexity, which cannot run on $N = 202,944$.
- **Required Fix:** Update all manuscript text, tables, and scripts to accurately describe the model as "SVM (SGD Modified Huber)" or "Linear Margin Classifier".

### Finding FND-03: Dual Hybrid Architecture Specification (High)
- **Affected Artifacts:** `models/hybrid/hybrid_meta_model.joblib` (50 features), `models/hybrid/failure_aware_hybrid.joblib` (27 features).
- **Empirical Evidence:**
  - Research model utilizes all 7 base models generating 21 probabilities + 21 confidence/uncertainty measures + 7 disagreement flags + 1 consensus count = 50 features.
  - Production dashboard model utilizes 5 base models generating 15 probabilities + 5 entropy + 5 margin + 1 disagreement score + 1 consensus count = 27 features.
- **Required Fix:** Formalize the dual architecture in `docs/supplementary/meta_feature_dictionary.csv`: the 50-feature model is the authoritative scientific research model; the 27-feature model is the lightweight operational deployment pipeline.
