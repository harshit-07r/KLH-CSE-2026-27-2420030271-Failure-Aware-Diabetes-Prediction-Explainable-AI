# Forensic Numerical Consistency and Provenance Report

**Audit Objective:** Investigate and resolve the reviewer-reported discrepancy between Table 6 (Probabilities-Only Ablation) and Table 2 (Standard Stacking).  
**Investigator:** Antigravity Forensic Audit Team  
**Evaluation Dataset:** Locked Test Set ($N = 50,736$, CDC BRFSS 2015, Seed 42)  

---

## 1. Resolution of the Table 6 vs. Table 2 Discrepancy

### The Reported Issue:
A reviewer identified that Table 6 (Probabilities-only ablation) reports:
- Macro-F1: **0.4199**
- Prediabetes Recall: **0.3402**

Whereas Table 2 (Standard Stacking) reports:
- Macro-F1: **0.4180**
- Prediabetes Recall: **0.4060**

### Empirical Forensic Investigation:
We audited the underlying serialized prediction file `TEST_PREDICTIONS_MASTER.csv` and recomputed multi-class metrics across all model prediction columns.

The mathematical root cause was identified with 100% precision:
1. **`Standard_Stacking_pred` (The Unweighted Baseline):**
   - In early pipeline development (Notebook 12 ablation script `gen_nb12_ablation.py`), the probabilities-only ablation baseline (M1) was trained using an unweighted `LogisticRegression(C=1.0)` meta-learner.
   - Evaluated on the locked test set, this unweighted model achieved:
     - **Accuracy:** **0.611716**
     - **Macro-F1:** **0.419926** (matches Table 6: **0.4199**)
     - **Balanced Accuracy:** **0.526027**
     - **Prediabetes Recall:** **0.340173** (matches Table 6: **0.3402**, identifying exactly 315 / 926 prediabetes cases).
2. **`Standard_Stacking_Corrected_pred` (The Balanced Weight Baseline):**
   - In subsequent pipeline refinement (`run_exp_audit_weight_fix.py`), the meta-learner was re-fitted with `class_weight='balanced'` on the OOF probability matrix to provide an equitable, apples-to-apples comparison against the class-weighted hybrid.
   - Evaluated on the exact same locked test set, this weight-corrected model achieved:
     - **Accuracy:** **0.600028**
     - **Macro-F1:** **0.417979** (matches Table 2: **0.4180**)
     - **Balanced Accuracy:** **0.527811**
     - **Prediabetes Recall:** **0.406048** (matches Table 2: **0.4060**, identifying exactly 376 / 926 prediabetes cases).

### Scientific Verdict:
The discrepancy was caused by comparing an **unweighted ablation baseline** against a **weight-corrected comparison model**.
- **No data was fabricated.**
- Both rows represent genuine, reproducible experimental evaluations of two distinct weighting regimes on the same locked test set.

### Required Manuscript Rectification:
In the revised manuscript:
- Table 2 must report the **Corrected Standard Stacking** (Acc 0.6000, Macro-F1 0.4180, Prediabetes Recall 0.4060) alongside the **Corrected Failure-Aware Hybrid** (Acc 0.6101, Macro-F1 0.4162, Prediabetes Recall 0.3888).
- Table 6 (Ablation Study) must report the ablation progression using the **same consistent class-weighting protocol** (M1 Corrected Baseline: Acc 0.6000, Macro-F1 0.4180 -> M4 Full Hybrid: Acc 0.6101, Macro-F1 0.4162).
- The historical unweighted baseline is documented transparently in `reports/audit/metric_provenance.csv`.

---

## 2. Authoritative Metrics Master Table ($N = 50,736$)

All values verified from `results/final/metrics_master.csv`:

| Model Name | Accuracy | Macro-F1 | Weighted-F1 | Balanced Acc | MCC | Log Loss | Brier Score | Prediab Recall | Prediab TP |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **SVM (SGD Mod Huber)** | **0.801364** | 0.447180 | 0.781203 | 0.471077 | 0.342217 | 0.4782 | **0.2841** | 0.004320 | 4 / 926 |
| **XGBoost** | 0.758081 | 0.434679 | 0.751104 | 0.468876 | 0.308014 | **0.4285** | 0.3120 | 0.020518 | 19 / 926 |
| **LightGBM** | 0.642995 | 0.423420 | 0.687421 | 0.516133 | 0.299888 | 0.5841 | 0.4215 | 0.253780 | 235 / 926 |
| **CatBoost** | 0.669426 | 0.429969 | 0.704218 | 0.512833 | 0.314862 | 0.5512 | 0.3984 | 0.182505 | 169 / 926 |
| **Random Forest** | 0.700351 | 0.430086 | 0.722105 | 0.498307 | 0.323046 | 0.5124 | 0.3621 | 0.077754 | 72 / 926 |
| **Logistic Regression** | 0.641379 | 0.425702 | 0.686512 | 0.518904 | 0.292016 | 0.6120 | 0.4328 | 0.323974 | 300 / 926 |
| **Decision Tree** | 0.581303 | 0.392616 | 0.648215 | 0.490191 | 0.248103 | 1.1245 | 0.5120 | 0.335853 | 311 / 926 |
| **Soft Voting** | 0.747674 | **0.447611** | 0.748210 | 0.502774 | **0.353318** | 0.4651 | 0.3211 | 0.042117 | 39 / 926 |
| **Standard Stacking (Original)** | 0.611716 | 0.419926 | 0.669812 | 0.526027 | 0.294614 | 0.6412 | 0.4412 | 0.340173 | 315 / 926 |
| **Standard Stacking (Corrected)**| 0.600028 | 0.417979 | 0.663102 | **0.527811** | 0.286243 | 0.6812 | 0.4721 | **0.406048** | **376 / 926** |
| **Hybrid (Original)** | 0.638738 | 0.424149 | 0.689215 | 0.523185 | 0.298312 | 0.6214 | 0.4312 | 0.295896 | 274 / 926 |
| **Hybrid (Corrected)** | 0.610099 | 0.416179 | 0.670518 | 0.521793 | 0.281960 | 0.6654 | 0.4589 | **0.388769** | 360 / 926 |

---

## 3. Label Mapping & Metric Conventions
- **Target Encoding:** $0 = \text{No Diabetes}, 1 = \text{Prediabetes}, 2 = \text{Diabetes}$.
- **Macro Averaging:** Unweighted arithmetic mean across all three classes: $\frac{1}{3} (F_0 + F_1 + F_2)$.
- **Zero Division:** Set to $0.0$ for precision when no positive instances are predicted.
- **Probability Matrix Format:** Multi-class softmax/sigmoid outputs normalized to sum to $1.0$ across the three columns.
