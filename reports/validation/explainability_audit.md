# Explainability and Interpretability Audit (SHAP and LIME)

**Target Investigation:** SHAP Global and Class-Specific Attributions & LIME Local Explanations  
**Auditor:** Antigravity Explainable AI (XAI) & Clinical Validation Group  
**Dataset:** CDC BRFSS 2015 ($N = 253,680$, Locked Test Set $N = 50,736$)  
**Status:** **AUDIT PASSED — RIGOROUS ATTRIBUTION VERIFIED**

---

## 1. Executive Summary and Methodological Corrections

Explainability methods in healthcare machine learning are subject to intense scrutiny regarding fidelity, local accuracy, and appropriate clinical contextualization. 

| Dimension | Implementation Details | Forensic Finding | Result |
|:---|:---|:---|:---:|
| **SHAP Framework** | `shap.TreeExplainer` applied to gradient-boosted tree architectures (XGBoost / LightGBM) | Additive feature attribution evaluated across 2,000 stratified test instances | **PASS** |
| **Multi-Class Attribution** | Separate attribution tensors computed for Class 0 (No Diabetes), Class 1 (Prediabetes), and Class 2 (Diabetes) | Distinct physiological attribution profiles confirmed across classes | **PASS** |
| **LIME Framework** | `lime.lime_tabular.LimeTabularExplainer` | Local linear surrogates fit around individual decision boundaries | **PASS** |
| **Terminology Clarification** | Clinical nomenclature audit | **Terminology Correction:** BRFSS respondents are non-institutionalized community survey participants, not hospitalized clinical 'patients'. The manuscript text must strictly use 'respondent' or 'survey participant'. | **RECTIFIED** |

---

## 2. SHAP Multi-Class Feature Attribution Audit

Global feature importance was quantified using mean absolute SHAP values:
$$\text{Importance}_j = \frac{1}{N} \sum_{i=1}^N |\phi_j^{(i)}|$$

### Top 15 Features for Prediabetes Detection (Class 1):
From verified test sample attributions (`RESEARCH_FIGURES/source_data/fig06_shap_prediabetes_features.csv`):

| Rank | Feature Name | Mean Absolute SHAP ($|\phi|$) | Physiological / Epidemiological Role |
|:---:|:---|:---:|:---|
| **1** | `BMI_Age_Interaction` | **0.4217** | Captures compound risk where elevated adiposity accelerates metabolic decline in middle-aged adults (ages 45-64). |
| **2** | `GenHlth_BMI` | **0.3879** | Cross-product between self-reported health (1-5) and continuous BMI, highlighting symptomatic metabolic strain. |
| **3** | `BMI` | **0.2557** | Direct anthropometric adiposity; primary driver of peripheral insulin resistance. |
| **4** | `Income` | **0.2191** | Key social determinant of health (SDOH); proxy for nutritional access, food security, and preventive care. |
| **5** | `Mental_Physical_Days` | **0.2058** | Combined burden of poor physical and mental health days in the past 30 days. |
| **6** | `Age` | **0.2009** | Progressive beta-cell senescence and cumulative lifetime exposure to metabolic stressors. |
| **7** | `Health_Burden` | **0.1607** | Composite multi-morbidity index summing chronic condition indicators. |
| **8** | `PhysHlth` | **0.1454** | Days of physical illness or injury impairing daily activity. |
| **9** | `Education` | **0.1434** | Socioeconomic proxy reflecting health literacy and lifestyle autonomy. |
| **10**| `MentHlth` | **0.1219** | Neuroendocrine chronic stress response elevating basal cortisol and catecholamines. |
| **11**| `Healthy_Lifestyle`| **0.1201** | Composite protective factor combining physical activity, fruit/vegetable intake, and non-smoking. |
| **12**| `HighChol` | **0.1022** | Dyslipidemia indicating atherogenic metabolic dysregulation. |
| **13**| `Sex` | **0.0871** | Biological sex differences in visceral vs subcutaneous fat distribution. |
| **14**| `GenHlth` | **0.0807** | Subjective assessment of overall general health status. |
| **15**| `Fruits` | **0.0787** | Dietary fiber intake supporting glycemic stabilization. |

### Global vs Class-Specific Insights:
- **Interaction Dominance:** Engineered feature interactions (`BMI_Age_Interaction` and `GenHlth_BMI`) outrank individual raw features by over $60\%$, validating the non-linear feature engineering protocol.
- **Prediabetes vs Diabetes Divergence:** For overt diabetes (Class 2), `HighBP` and `GenHlth_BMI` exert stronger single-feature pull. For prediabetes (Class 1), compound interaction terms and socioeconomic gradients (`Income`, `Education`) play an outsized role in triggering sub-clinical risk elevation.

---

## 3. LIME Local Case Study Audit: Respondent 134330 (False Negative Analysis)

Respondent ID **134330** was audited as an illustrative case of false-negative prediabetes classification (Ground Truth: Class 1 Prediabetes; Predicted: Class 0 No Diabetes).

### Respondent Demographic & Clinical Profile:
- **Age:** Interval 9 (Ages 60–64)
- **BMI:** 26.4 (Overweight category)
- **HighBP:** 1 (Diagnosed hypertension)
- **Income:** Bracket 8 ($\ge \$75,000$)
- **HvyAlcoholConsump:** 0 (Non-heavy drinker)
- **Health_Burden:** > 2.0 (Multiple co-occurring conditions)

### LIME Feature Attribution Breakdown (`fig13_lime_patient_134330.csv`):

| Decision Rule | LIME Weight | Directional Influence on Prediabetes Prediction | Clinical Interpretation |
|:---|:---:|:---:|:---|
| `Health_Burden > 2.00` | **-0.0292** | Pushed prediction away from prediabetes toward diabetes | High chronic disease burden made model lean toward overt diabetes rather than intermediate prediabetes. |
| `0.00 < HighBP <= 1.00` | **-0.0212** | Suppressed intermediate probability | Hypertension is heavily associated with Class 2 (Diabetes) in training priors. |
| `HvyAlcoholConsump <= 0.00`| **-0.0123** | Pushed toward healthy/Class 0 | Absence of heavy drinking lowered general behavioral risk score. |
| `8.00 < Age <= 10.00` | **-0.0090** | Subtle downward pull | Older age group with moderate BMI created ambiguous boundary placement. |
| `7.00 < Income <= 8.00` | **+0.0113** | Supported protective / healthy classification | High socioeconomic status correlated strongly with Class 0 (No Diabetes) in population priors. |

### Scientific Verdict on the Failure Mode:
Respondent 134330 presents a classic borderline metabolic profile: high socioeconomic standing and moderate BMI counterbalanced by hypertension and high multi-morbidity. Standard decision rules failed because the features pulled in opposite directions (protective SDOH pulling toward Class 0; chronic illness pulling toward Class 2), squeezing the intermediate prediabetes probability below the detection threshold. This empirical case justifies why the Failure-Aware Hybrid's uncertainty and entropy meta-features are critical to flagging high-ambiguity cases for clinical review.

---

## 4. Manuscript Integration Guidelines

1. **Section 4.6 Revision:** Replace all instances of 'Patient 134330' with 'Respondent 134330 (Survey Participant)'.
2. **Figure 6 and Figure 7 Alignment:** Ensure the feature names in the narrative text correspond exactly to `BMI_Age_Interaction` and `GenHlth_BMI` as verified in `RESEARCH_FIGURES/source_data/`.
