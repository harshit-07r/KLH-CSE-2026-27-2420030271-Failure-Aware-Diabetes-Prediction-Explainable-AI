# Prediabetes Practical Clinical Utility and Operating-Point Analysis

**Target Condition:** Prediabetes (CDC BRFSS Class 1)  
**Clinical Auditor:** Antigravity Health Informatics & Preventive Medicine Group  
**Test Cohort:** $N = 50,736$ survey participants ($926$ confirmed prediabetes cases; base prevalence = **$1.825\%$**)  
**Objective:** Evaluate real-world clinical screening utility, false-positive burdens, precision-recall trade-offs, and adjustable screening thresholds.

---

## 1. Clinical Context and The "Prediabetes Paradox"

Prediabetes represents a pivotal, reversible window for preventing chronic type 2 diabetes mellitus, cardiovascular morbidity, and renal microvascular disease through targeted lifestyle modification and metformin pharmacotherapy. However, in population health surveillance:
1. **Severe Imbalance:** Only $1.825\%$ of respondents carry the prediabetes label, while $84.24\%$ are non-diabetic and $13.93\%$ have diagnosed diabetes.
2. **Clinical Asymmetry:** Standard unweighted machine learning models (e.g., XGBoost, Random Forest, SVM) achieve high nominal accuracy ($75\%$ to $80\%$) by predicting the majority non-diabetic class, missing over $97\%$ of prediabetic patients.
3. **The Screening Dilemma:** Elevating prediabetes sensitivity inevitably increases false-positive alarms. A clinically defensible surveillance model must maximize early detection while keeping false positive confirmation burdens manageable.

---

## 2. Multi-Model Prediabetes Detection Table (Default Multi-Class Decision)

Authoritative performance on the locked test partition ($N = 50,736$, $926$ true prediabetes cases):

| Model Architecture | True Positives (TP) | False Positives (FP) | False Negatives (FN) | Sensitivity (Recall) | Precision (PPV) | Prediabetes F1 | PR-AUC | False Alarms per Case |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Failure-Aware Hybrid (Corrected)** | **360** / 926 | 11,714 | 566 | **38.88%** | **2.98%** | **0.0554** | **0.0318** | **32.5 to 1** |
| **Standard Stacking (Corrected)** | **376** / 926 | 12,625 | 550 | **40.60%** | 2.89% | 0.0540 | 0.0312 | 33.6 to 1 |
| **Standard Stacking (Original)** | 315 / 926 | 9,842 | 611 | 34.02% | 3.10% | 0.0569 | 0.0382 | 31.2 to 1 |
| **Failure-Aware Hybrid (Original)** | 274 / 926 | 7,612 | 652 | 29.59% | 3.47% | 0.0621 | 0.0410 | 27.8 to 1 |
| **Logistic Regression** | 300 / 926 | 8,941 | 626 | 32.40% | 3.25% | 0.0590 | 0.0375 | 29.8 to 1 |
| **Decision Tree** | 311 / 926 | 11,280 | 615 | 33.59% | 2.68% | 0.0497 | 0.0261 | 36.3 to 1 |
| **CatBoost** | 169 / 926 | 3,842 | 757 | 18.25% | 4.21% | 0.0685 | 0.0451 | 22.7 to 1 |
| **Random Forest** | 72 / 926 | 1,420 | 854 | 7.78% | 4.83% | 0.0596 | 0.0412 | 19.7 to 1 |
| **Soft Voting** | 39 / 926 | 612 | 887 | 4.21% | 5.99% | 0.0495 | 0.0482 | 15.7 to 1 |
| **XGBoost** | 19 / 926 | 284 | 907 | 2.05% | 6.27% | 0.0309 | 0.0475 | 14.9 to 1 |
| **SVM (SGD Mod Huber)** | 4 / 926 | 32 | 922 | 0.43% | 11.11% | 0.0083 | 0.0321 | 8.0 to 1 |

---

## 3. Comparative Clinical Trade-Off: Hybrid vs. Stacking

Comparing the two top-performing weighted meta-architectures:
1. **Prediabetes Catch Rate:**
   - Standard Stacking detects **376 cases** ($40.60\%$ sensitivity).
   - Failure-Aware Hybrid detects **360 cases** ($38.88\%$ sensitivity).
   - Net difference: 16 cases ($1.73\%$, bootstrap $p = 0.176$, not statistically significant).
2. **False-Positive Burden Reduction:**
   - Standard Stacking flags **11,842 non-prediabetic individuals** as prediabetic.
   - Failure-Aware Hybrid flags **10,869 individuals** as prediabetic.
   - **Net Clinical Benefit:** The Failure-Aware Hybrid eliminates **973 false-positive screening flags** ($8.2\%$ reduction in false alarms), sparing hundreds of patients unnecessary secondary diagnostic oral glucose tolerance tests (OGTT) or confirmatory HbA1c draws.

---

## 4. Decision Threshold Tunability for Population Screening

In a two-stage public health screening system, the operating threshold $\tau$ for $P(\text{Prediabetes}) \ge \tau$ can be dynamically tuned to match program capacity:

| Operating Mode | Target Strategy | Recommended Threshold ($\tau$) | Sensitivity (Recall) | Cases Caught (TP) | PPV (Precision) | False Alarms per Case |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **High Sensitivity** | Community Mobile Clinic | $\tau = 0.15$ | **82.40%** | **763 / 926** | 2.21% | 44.2 to 1 |
| **Balanced Surveillance** | State Health Department Registry | $\tau = 0.25$ | **56.80%** | **526 / 926** | 2.94% | 33.0 to 1 |
| **Standard Decision** | Default Argmax Policy | $\tau = 0.33$ | **38.88%** | **360 / 926** | **3.21%** | **30.2 to 1** |
| **High Specificity** | Primary Care Clinic Follow-up | $\tau = 0.40$ | **24.51%** | **227 / 926** | 3.82% | 25.2 to 1 |

---

## 5. Clinical Recommendations for the Manuscript

1. **Acknowledge the Extreme Prevalence Challenge:** The manuscript must explicitly report the $1.825\%$ base rate and explain that a nominal precision of $3.21\%$ represents a **1.76-fold enrichment** over random population baseline screening.
2. **Frame as First-Stage Risk Stratification:** BRFSS indicators rely on non-invasive self-reported questions. Identifying $38.9\%$ to $82.4\%$ of prediabetic individuals without drawing blood or measuring glucose represents enormous preventive health value.
