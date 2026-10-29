# End-to-End Artifact Lineage and Data Provenance

This document maps the complete deterministic pipeline from raw survey data to locked-test evaluation metrics and publication figures:

```text
========================================================================================
                                 PIPELINE DATA FLOW
========================================================================================
[1. RAW INGESTION]
   diabetes_012_health_indicators_BRFSS2015.csv (N = 253,680 x 22)
          │
          ▼  Notebook 02: Verification of zero missing values; Stratified 80/20 split (Seed 42)
[2. DATA PARTITIONS]
   Train Set: N = 202,944 (80%)  │  Locked Test Set: N = 50,736 (20%)
          │
          ▼  Notebook 05: Apply 8 clinical formulas (BMI_Category, Health_Burden, etc.)
[3. FEATURE ENGINEERING]
   df1_engineered.csv (N = 253,680 x 30: 29 predictors + Diabetes_012)
          │
          ▼  Notebook 08: Stratified 5-Fold CV (Seed 42) on Train Set (N = 202,944)
[4. BASE MODEL TRAINING & OOF GENERATION]
   7 Base Estimators: LR, DT, RF, SGD (Mod Huber), XGBoost, LightGBM, CatBoost
   Out-of-Fold Matrix: 202,944 x 21 probabilities
   Test Prediction Matrix: 50,736 x 21 probabilities
          │
          ▼  Notebook 12: Construct 50 Meta-Features (Uncertainty, Margin, Disagreement, Consensus)
[5. META-FEATURE TRANSFORMATION]
   Train Meta-Matrix: 202,944 x 50 (from OOF predictions - ZERO TEST LEAKAGE)
   Test Meta-Matrix:  50,736 x 50  (from frozen base models evaluated on locked test set)
          │
          ▼  Notebook 12: Train Meta-Learner LogisticRegression(class_weight='balanced', C=1.0)
[6. META-LEARNER EVALUATION]
   TEST_PREDICTIONS_MASTER.csv (N = 50,736 rows x evaluated model predictions)
          │
          ├──► Notebook 10: Multi-class metrics (results/final/metrics_master.csv)
          ├──► Notebook 13: SHAP TreeExplainer (2,000 samples) & LIME (Patient 134330)
          ├──► Notebook 14: Subgroup fairness & Calibration reliability curves
          └──► RESEARCH_FIGURES: 22 publication figures (PNG 300 DPI + SVG vector)
========================================================================================
```
