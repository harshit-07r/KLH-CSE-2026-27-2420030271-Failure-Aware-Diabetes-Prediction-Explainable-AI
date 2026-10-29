# Pipeline Reproducibility and Environment Specification

**Pipeline Name:** Three-Class Diabetes Status Surveillance Pipeline  
**Codebase Root:** `d:\DAV\AI_Driven_Public_Health_Surveillance`  
**Execution Environment:** Python 3.12, Windows 11 x64  
**Date:** 2026-10-29  

---

## 1. Environment & Dependency Specifications

All models and evaluations are reproducible with deterministic seeds under the following package specifications:

| Library | Version | Role in Pipeline | Deterministic Seed Flag |
|:---|:---:|:---|:---:|
| **Python** | 3.12.4 | Runtime interpreter | `PYTHONHASHSEED=42` |
| **numpy** | 1.26.4 | Numerical arrays & linear algebra | `np.random.seed(42)` |
| **pandas** | 2.2.2 | Data handling & metric persistence | N/A |
| **scikit-learn** | 1.4.2 | Logistic Regression, Decision Tree, Random Forest, SGDClassifier, Metrics | `random_state=42` |
| **xgboost** | 2.0.3 | Gradient boosted decision trees | `random_state=42` |
| **lightgbm** | 4.3.0 | Fast histogram-based gradient boosting | `random_state=42` |
| **catboost** | 1.2.3 | Symmetric tree gradient boosting | `random_seed=42` |
| **scipy** | 1.13.0 | Shannon entropy and statistical testing | N/A |
| **joblib** | 1.4.0 | Model serialization and parallel CV execution | N/A |

---

## 2. Global Pipeline Seed Registry

The following random seed protocol guarantees end-to-end exact reproducibility:

- **Train/Test Split:** `random_state = 42`
- **5-Fold Stratified K-Fold:** `random_state = 42`, `shuffle = True`
- **Base Estimators:**
  - `LogisticRegression(random_state=42)`
  - `DecisionTreeClassifier(random_state=42)`
  - `RandomForestClassifier(random_state=42)`
  - `SGDClassifier(random_state=42)`
  - `XGBClassifier(random_state=42)`
  - `LGBMClassifier(random_state=42)`
  - `CatBoostClassifier(random_seed=42)`
- **Meta-Learner:** `LogisticRegression(random_state=42)`
- **Bootstrap Verification:** `random_state = 42` (paired sample index generation)

---

## 3. Directory Layout and Verification Artefacts

```
AI_Driven_Public_Health_Surveillance/
├── data/
│   ├── raw/
│   │   └── diabetes_012_health_indicators_BRFSS2015.csv  [N=253,680]
│   └── processed/
│       ├── df1_engineered.csv                             [N=253,680]
│       ├── train_indices.npy                              [N=202,944]
│       └── test_indices.npy                               [N=50,736]
├── models/
│   ├── base_models/                                       [7 serialized base estimators]
│   └── hybrid/
│       ├── failure_aware_hybrid.joblib                    [Authoritative Pipeline]
│       └── hybrid_meta_model.joblib                       [Meta-learner weights]
├── results/
│   └── final/
│       ├── metrics_master.csv                             [Authoritative Multi-class Metrics]
│       └── confusion_matrices/                            [12 model CM CSVs]
├── docs/
│   └── supplementary/
│       ├── meta_feature_dictionary.csv                    [50 meta-features verified]
│       └── model_configuration_registry.csv               [12 model hyperparameters]
└── reports/
    └── audit/
        ├── leakage_audit.md                               [Leakage audit report]
        ├── numerical_consistency_report.md                [Table 6 vs 2 resolution]
        └── metric_provenance.csv                          [Weighting protocol provenance]
```

---

## 4. Execution Command for Authoritative Metrics

To reproduce the exact authoritative multi-class metrics:

```powershell
python -c "import pandas as pd; from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score; df = pd.read_csv('TEST_PREDICTIONS_MASTER.csv'); y_true = df['y_true']; y_pred = df['Production_Hybrid_Corrected_pred']; print('Accuracy:', accuracy_score(y_true, y_pred)); print('Macro-F1:', f1_score(y_true, y_pred, average='macro')); print('Balanced Acc:', balanced_accuracy_score(y_true, y_pred))"
```
