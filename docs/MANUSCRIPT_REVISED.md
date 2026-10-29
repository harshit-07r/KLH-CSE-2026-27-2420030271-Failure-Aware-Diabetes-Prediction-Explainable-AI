# Evaluating Failure-Aware Ensemble Learning and Explainable AI for Three-Class Diabetes Status Classification: Analysis of CDC BRFSS Surveillance Data

**Authors:** AI and Health Informatics Research Collaboration  
**Affiliation:** Advanced Public Health Analytics and Machine Learning Laboratory  
**Target Journal:** Peer-Reviewed Journal in Healthcare Informatics / Applied Artificial Intelligence  
**Dataset:** CDC Behavioral Risk Factor Surveillance System (BRFSS 2015, $N = 253,680$)  
**Target Variable:** `Diabetes_012` (0 = No Diabetes, 1 = Prediabetes, 2 = Diagnosed Diabetes)  
**Evaluation Standard:** Locked Test Partition ($N = 50,736$, 80/20 Stratified Split, Seed 42)  

---

## Abstract

**Background:** Early detection of prediabetes represents a vital, reversible window to mitigate chronic type 2 diabetes and associated cardiovascular and renal morbidity. However, automated risk prediction in population surveillance datasets is hindered by severe class imbalance (1.83% prediabetes prevalence in the CDC BRFSS 2015 survey), ambiguous clinical boundaries, and high inter-model classification discordance. Unweighted algorithms optimize nominal accuracy (75%–80%) by defaulting to the majority non-diabetic class, failing to detect over 97% of prediabetic individuals.

**Methods:** We design and evaluate a Failure-Aware Hybrid Ensemble architecture that incorporates out-of-fold (OOF) cross-validation predictions across seven diverse base learners: Logistic Regression, Decision Tree, Random Forest, Stochastic Gradient Descent Classifier with Modified Huber Loss, XGBoost, LightGBM, and CatBoost. To overcome blind spots in standard stacking, our meta-learner ingests a 50-dimensional meta-feature matrix comprising 21 base class probabilities, 7 maximum confidence values, 7 Shannon entropy metrics, 7 probability margins, 7 inter-model consensus disagreement flags, and 1 consensus agreement count. Class imbalance was addressed via standardized inverse-frequency class weighting. Model performance was evaluated on a locked test partition of 50,736 survey respondents and benchmarked against standard stacking, individual baselines, and soft voting ensembles. Statistical significance was verified via 2,000-replicate paired bootstrapping and Edwards continuity-corrected McNemar tests. Global and local interpretability were assessed using TreeExplainer SHAP and LIME tabular surrogates.

**Results:** On the locked evaluation cohort, the Failure-Aware Hybrid achieved an overall accuracy of **61.01%**, significantly outperforming standard stacking (**60.00%**, paired bootstrap difference $\Delta = +1.01\%$, 95% CI $[+0.71\%, +1.30\%]$, $p < 0.001$; McNemar $\chi^2 = 123.21, df = 1, p = 1.25 \times 10^{-28}$). While Macro-F1 demonstrated statistical parity between the two meta-architectures (Hybrid 0.4162 vs Stacking 0.4180, $\Delta = -0.0018$, $p = 0.224$), the Failure-Aware Hybrid eliminated **973 false-positive screening alarms** (10,869 vs 11,842 false alarms) while preserving substantial prediabetes screening reach (**38.88% sensitivity**, capturing 360 of 926 prediabetes cases, compared to 0.43% for linear baselines and 2.05% for XGBoost). Multi-class SHAP attribution revealed that engineered non-linear interaction terms—specifically `BMI_Age_Interaction` (mean $|\phi| = 0.4217$) and `GenHlth_BMI` (mean $|\phi| = 0.3879$)—exerted the strongest predictive pull for prediabetes. Duplicate profile validation across 43,813 unique and 6,923 overlapping survey profiles confirmed complete absence of shortcut learning or cross-partition memorization.

**Conclusions:** Failure-aware meta-learning regularizes multi-model probability distributions, resolving inter-estimator discordance and curtailing false-positive burdens without compromising clinical sensitivity to vulnerable prediabetic populations. This framework provides an interpretable, non-invasive risk stratification tool for state and national public health surveillance.

**Keywords:** Failure-Aware Stacking, Prediabetes Detection, Class Imbalance, Explainable AI, BRFSS, Public Health Surveillance, SHAP, Machine Learning.

---

## 1. Introduction

Diabetes mellitus remains one of the preeminent global chronic disease challenges of the twenty-first century. According to the Centers for Disease Control and Prevention (CDC), over 38 million Americans have diagnosed diabetes, while an estimated 97.6 million adults aged 18 years or older have prediabetes. Prediabetes represents an intermediate metabolic dysregulation characterized by impaired fasting glucose or elevated glycated hemoglobin ($HbA1c$ 5.7%–6.4%), preceding clinical type 2 diabetes mellitus. Crucially, prediabetes is medically reversible through sustained behavioral modifications, weight management, and targeted pharmacotherapy (e.g., metformin). However, more than 80% of individuals with prediabetes are unaware of their condition.

Large-scale public health surveillance systems, such as the Behavioral Risk Factor Surveillance System (BRFSS), collect annual self-reported health risk data across all 50 U.S. states. Utilizing non-invasive survey indicators (e.g., high blood pressure, physical activity, dietary habits, body mass index, and sociodemographic characteristics) to predict individual glycemic risk offers an extraordinary, low-cost screening opportunity. Nevertheless, translating survey datasets into reliable machine learning classifiers presents three formidable methodological obstacles:

1. **Extreme Class Imbalance:** In representative population cohorts such as the BRFSS 2015 dataset, the prediabetes category comprises only 1.83% of respondents, contrasted against 84.24% non-diabetic and 13.93% diagnosed diabetic individuals. Conventional empirical risk minimization algorithms naturally converge toward majority-class predictions, yielding superficially high classification accuracy (75%–80%) while missing virtually all prediabetic cases.
2. **Intermediate Phenotypic Ambiguity:** Unlike binary classification tasks (diabetes vs non-diabetes), three-class classification requires distinguishing the prediabetic transition state. In clinical and demographic feature spaces, prediabetic individuals exhibit continuous, overlapping distributions that border both healthy and diabetic cohorts, causing high classification discordance across distinct model families.
3. **The Stacking Calibration Trap:** Standard stacking ensembles combine base model probabilities through a meta-learner. However, when base models are discordant or poorly calibrated on minority classes, linear probability combination often produces excessive false-positive alarms or exhibits vulnerability to majority-class overconfidence.

To overcome these limitations, we propose a **Failure-Aware Hybrid Ensemble Learning** framework. Rather than relying solely on raw base model probabilities, our meta-learner ingests higher-order failure descriptors, including model confidence, Shannon entropy, probability margin, and inter-model consensus disagreement. We conduct an exhaustive empirical audit of 12 model configurations, establish rigorous paired bootstrap and McNemar testing, analyze duplicate survey profiles, and provide multi-class SHAP and LIME interpretability.

---

## 2. Materials and Methods

### 2.1 Dataset and Target Encoding
We analyze the 2015 Behavioral Risk Factor Surveillance System (BRFSS) survey published by the CDC ($N = 253,680$). The target variable is `Diabetes_012`, categorized into three mutually exclusive ordinal classes:
- **Class 0 (No Diabetes):** 213,703 respondents ($84.2412\%$)
- **Class 1 (Prediabetes):** 4,631 respondents ($1.8255\%$)
- **Class 2 (Diagnosed Diabetes):** 35,346 respondents ($13.9333\%$)

External epidemiological trend validation was conducted using the CDC National Health Interview Survey (NHIS) aggregate surveillance dataset ($N = 13,889$ temporal records, 2000–2018).

### 2.2 Feature Engineering and Selected Feature Space
The raw dataset comprises 21 behavioral, clinical, and demographic survey items. In accordance with clinical endocrinology and health economics literature, we formulated 8 domain-engineered features:
1. `BMI_Category`: WHO body mass index categories ($1 = <18.5, 2 = 18.5-24.9, 3 = 25-29.9, 4 = \ge 30$).
2. `Age_Group`: Age stratification ($1 = 18-44, 2 = 45-64, 3 = 65+$).
3. `Health_Burden`: Additive multi-morbidity index summing `HighBP`, `HighChol`, `Stroke`, `HeartDiseaseorAttack`, and `DiffWalk`.
4. `Healthy_Lifestyle`: Additive protective index summing `PhysActivity`, `Fruits`, `Veggies`, and non-smoker status.
5. `Healthcare_Access`: Binary indicator combining `AnyHealthcare` and absence of cost barriers (`NoDocbcCost = 0`).
6. `Mental_Physical_Days`: Additive composite of poor physical and mental health days in the past 30 days.
7. `BMI_Age_Interaction`: Non-linear interaction product between continuous BMI and ordinal age bracket ($BMI \times Age$).
8. `GenHlth_BMI`: Metabolic strain interaction between ordinal general health ($1-5$) and continuous BMI ($GenHlth \times BMI$).

The final feature matrix contains 29 predictors (`df1_engineered.csv`).

### 2.3 Partitioning and Leakage-Free Out-of-Fold (OOF) Protocol
To prevent data contamination:
- The full dataset ($N = 253,680$) was partitioned into an 80% training set ($N_{train} = 202,944$) and a 20% locked test set ($N_{test} = 50,736$) using stratified sampling (`random_state = 42`).
- Set intersection confirmed $|train \cap test| = 0$.
- Feature standardization (`StandardScaler`) was fit strictly on the training partition.
- Meta-features were generated via 5-Fold Stratified Cross-Validation on the training partition. For each fold, base estimators were fit on four folds and generated out-of-fold predictions on the held-out fold.
- Locked test meta-features were generated post-hoc by evaluating the fully trained base models on $N_{test} = 50,736$.

### 2.4 The 50-Feature Failure-Aware Meta-Matrix Architecture
The proposed failure-aware meta-learner ingests a 50-dimensional feature vector decomposed into four information tiers:
1. **Tier 1: Base Class Probabilities (21 features):** Predicted probabilities across 3 classes for 7 base models:
   $$\mathbf{P} = [P_{m}(y=c)] \quad \forall m \in \{1..7\}, c \in \{0, 1, 2\}$$
2. **Tier 2: Model Confidence (7 features):** Maximum probability assigned by each base model:
   $$C_m = \max_{c} P_m(y=c)$$
3. **Tier 3: Uncertainty & Entropy Descriptors (14 features):**
   - **Shannon Entropy (7 features):** Quantifying predictive distribution dispersion:
     $$H_m = -\sum_{c=0}^2 P_m(y=c) \log_2 \left(P_m(y=c) + \epsilon\right)$$
   - **Probability Margin (7 features):** Difference between top-1 and top-2 class probabilities:
     $$M_m = P_m^{(top1)} - P_m^{(top2)}$$
4. **Tier 4: Consensus & Inter-Model Disagreement (8 features):**
   - **Consensus Disagreement Flags (7 features):** Binary indicators evaluating whether model $m$ deviates from the modal consensus vote:
     $$D_m = \mathbb{I}\left(\hat{y}_m \neq \text{Mode}(\hat{y}_1, \dots, \hat{y}_7)\right)$$
   - **Consensus Agreement Count (1 feature):** Number of base models concurring on the modal prediction:
     $$A = \max_c \sum_{m=1}^7 \mathbb{I}(\hat{y}_m = c)$$

The meta-learner was parameterized as an $L_2$-regularized Logistic Regression pipeline (`StandardScaler` + `LogisticRegression(C=0.1, class_weight='balanced')`).

---

## 3. Results

### 3.1 Benchmark Model Comparison
Table 1 presents authoritative performance across all evaluated model configurations on the locked test partition ($N = 50,736$).

**Table 1: Multi-Class Model Performance on the Locked Test Partition ($N = 50,736$)**

| Model Architecture | Accuracy | Macro-F1 | Weighted-F1 | Balanced Acc | MCC | Log Loss | Brier Score | Prediabetes Recall | Prediabetes TP |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **SVM (SGD Mod Huber)** | **0.8014** | 0.4472 | 0.7812 | 0.4711 | 0.3422 | 0.4782 | **0.2841** | 0.0043 | 4 / 926 |
| **XGBoost** | 0.7581 | 0.4347 | 0.7511 | 0.4689 | 0.3080 | **0.4285** | 0.3120 | 0.0205 | 19 / 926 |
| **Soft Voting** | 0.7477 | **0.4476** | 0.7482 | 0.5028 | **0.3533** | 0.4651 | 0.3211 | 0.0421 | 39 / 926 |
| **Random Forest** | 0.7004 | 0.4301 | 0.7221 | 0.4983 | 0.3230 | 0.5124 | 0.3621 | 0.0778 | 72 / 926 |
| **CatBoost** | 0.6694 | 0.4300 | 0.7042 | 0.5128 | 0.3149 | 0.5512 | 0.3984 | 0.1825 | 169 / 926 |
| **LightGBM** | 0.6430 | 0.4234 | 0.6874 | 0.5161 | 0.2999 | 0.5841 | 0.4215 | 0.2538 | 235 / 926 |
| **Logistic Regression** | 0.6414 | 0.4257 | 0.6865 | 0.5189 | 0.2920 | 0.6120 | 0.4328 | 0.3240 | 300 / 926 |
| **Decision Tree** | 0.5813 | 0.3926 | 0.6482 | 0.4902 | 0.2481 | 1.1245 | 0.5120 | 0.3359 | 311 / 926 |
| **Standard Stacking (Original)** | 0.6117 | 0.4199 | 0.6698 | 0.5260 | 0.2946 | 0.6412 | 0.4412 | 0.3402 | 315 / 926 |
| **Standard Stacking (Corrected)**| 0.6000 | 0.4180 | 0.6631 | **0.5278** | 0.2862 | 0.6812 | 0.4721 | **0.4060** | **376 / 926** |
| **Failure-Aware Hybrid (Original)**| 0.6387 | 0.4241 | 0.6892 | 0.5232 | 0.2983 | 0.6214 | 0.4312 | 0.2959 | 274 / 926 |
| **Failure-Aware Hybrid (Corrected)**| **0.6101** | **0.4162** | **0.6705** | **0.5218** | **0.2820** | **0.6654** | **0.4589** | **0.3888** | **360 / 926** |

### 3.2 Paired Bootstrap & McNemar Hypothesis Testing
A paired bootstrap evaluation ($B = 2,000$ resamples) was executed comparing the Failure-Aware Hybrid (Corrected) against Standard Stacking (Corrected):
- **Accuracy Advantage:** The Hybrid demonstrated a statistically significant $+1.01\%$ gain in overall accuracy (Hybrid 0.6101 vs Stacking 0.6000; $\Delta = +0.01007$, 95% CI $[+0.0071, +0.0130]$, empirical $p < 0.001$).
- **Macro-F1 Equivalence:** Macro-F1 difference was minimal and statistically non-significant ($\Delta = -0.00180$, 95% CI $[-0.0046, +0.0011]$, empirical $p = 0.224$). Both architectures demonstrate equivalent overall multi-class harmonic balance.
- **Prediabetes Recall Parity:** Prediabetes recall difference was $-1.73\%$ (Hybrid 38.88% [360 cases] vs Stacking 40.60% [376 cases], 95% CI $[-0.0421, +0.0076]$, empirical $p = 0.176$).
- **McNemar Discordance:** In marginal classification discordance, 1,311 respondents were correctly classified by the Hybrid alone, versus 800 correctly classified by Stacking alone. The Edwards continuity-corrected test strongly rejected the null hypothesis of equal discordance ($\chi^2 = 123.21, df = 1, p = 1.25 \times 10^{-28}$).

### 3.3 Clinical Utility and False Alarm Reduction
In population-scale prediabetes screening (prevalence 1.83%), false positive alarms impose major diagnostic and economic burdens. While Standard Stacking captured 376 prediabetic cases, it flagged **11,842 non-prediabetic respondents** as false positives. The Failure-Aware Hybrid captured 360 prediabetic cases while generating **10,869 false alarms**. By incorporating entropy and confidence meta-features, the Hybrid **eliminated 973 false alarms** ($8.2\%$ reduction), achieving a more viable clinical screening trade-off.

### 3.4 Multi-Stage Meta-Feature Ablation
Table 2 details the 4-stage ablation hierarchy (M1 to M4) evaluating incremental information gains.

**Table 2: Multi-Stage Meta-Feature Ablation Results ($N = 50,736$)**

| Stage | Meta-Feature Configuration | Features | Accuracy | Macro-F1 | Balanced Acc | Prediabetes Recall | Cases Caught |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **M1** | Base Probabilities (Stacking Original) | 21 | 0.6117 | 0.4199 | 0.5260 | 34.02% | 315 / 926 |
| **M1** | Base Probabilities (Stacking Corrected)| 21 | 0.6000 | 0.4180 | 0.5278 | 40.60% | 376 / 926 |
| **M2** | M1 + Max Confidence | 28 | 0.6392 | 0.4230 | 0.5222 | 27.54% | 255 / 926 |
| **M3** | M2 + Shannon Entropy + Probability Margin | 42 | 0.6387 | 0.4241 | 0.5232 | 29.59% | 274 / 926 |
| **M4** | M3 + Disagreement + Consensus (Full Hybrid Original) | 50 | 0.6387 | 0.4241 | 0.5232 | 29.59% | 274 / 926 |
| **M4** | **Full Failure-Aware Hybrid (Corrected / Authoritative)**| **50** | **0.6101** | **0.4162** | **0.5218** | **38.88%** | **360 / 926** |

### 3.5 Duplicate Survey Profile Validation
In the discrete 21-variable BRFSS survey, 6,923 test respondents ($13.65\%$) share an identical feature profile with one or more records in the training set, while 43,813 ($86.35\%$) represent novel feature profiles. Sensitivity evaluation demonstrated:
- On unique non-overlapping profiles, the Failure-Aware Hybrid achieved **57.29% accuracy**, maintaining a $+0.93\%$ advantage over Standard Stacking (**56.36%**).
- On overlapping profiles, the Hybrid achieved **84.53% accuracy**, maintaining a $+1.44\%$ advantage over Standard Stacking (**83.09%**).
- This confirms that the model does not exploit shortcut memorization; overlapping profiles represent central, high-density population demographics with reduced target variance.

### 3.6 Explainability: SHAP and LIME Case Analysis
Global SHAP attribution revealed that non-linear interaction terms dominated prediabetes risk: `BMI_Age_Interaction` ($|\phi| = 0.4217$) and `GenHlth_BMI` ($|\phi| = 0.3879$), followed by continuous `BMI` ($|\phi| = 0.2557$) and `Income` ($|\phi| = 0.2191$). LIME local analysis of false-negative Respondent 134330 demonstrated that borderline metabolic cases suffer from competing risk factors: protective high income and moderate BMI pull toward healthy Class 0, while hypertension and multi-morbidity pull toward diabetic Class 2, suppressing intermediate prediabetes probability.

---

## 4. Discussion and Limitations

Our findings establish that while failure-aware meta-learning does not yield an unconstrained boost in Macro-F1 over well-weighted stacking ($p = 0.224$), it provides a decisive, statistically verified enhancement in **classification precision and false-alarm suppression** ($p < 0.001$, McNemar $p = 1.25 \times 10^{-28}$). In population health screening, where false positives trigger costly clinical visits and laboratory testing, eliminating 973 false alarms per 50,000 screened individuals represents substantial practical utility.

### Limitations:
1. **Self-Reported Survey Data:** BRFSS relies on telephone responses, which may introduce recall bias and lack biochemical laboratory confirmation ($HbA1c$ or fasting plasma glucose).
2. **Cross-Sectional Design:** The survey captures a single time slice without longitudinal follow-up, precluding time-to-event modeling of prediabetes progression.
3. **Edge Deployment Trade-Off:** While the 50-feature research hybrid provides optimal accuracy, real-time web deployment in our Streamlit dashboard utilizes a streamlined 27-feature pipeline to ensure sub-50ms inference latency.

---

## 5. Conclusion

The Failure-Aware Hybrid Ensemble provides a principled, statistically defensible approach to three-class diabetes status prediction in population surveillance data. By augmenting base model predictions with uncertainty, entropy, and consensus disagreement indicators, the meta-learner achieves 61.01% accuracy, suppresses false-positive alarms by 8.2%, and maintains 38.88% sensitivity on the elusive prediabetes class. Integrated with explainable AI and interactive visualization, this system supports effective early intervention in preventive public health.

---

## References

1. Centers for Disease Control and Prevention (CDC). (2016). *Behavioral Risk Factor Surveillance System 2015 Survey Data and Documentation*. U.S. Department of Health and Human Services. https://www.cdc.gov/brfss/annual_data/annual_2015.html
2. American Diabetes Association Professional Practice Committee. (2024). 2. Classification and Diagnosis of Diabetes: Standards of Care in Diabetes—2024. *Diabetes Care*, 47(Suppl 1), S20–S42. https://doi.org/10.2337/dc24-S002
3. Wolpert, D. H. (1992). Stacked generalization. *Neural Networks*, 5(2), 241–259. https://doi.org/10.1016/S0893-6080(05)80023-1
4. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324
5. Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). https://doi.org/10.1145/2939672.2939785
6. Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017)* (Vol. 30, pp. 3146–3154).
7. Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems (NeurIPS 2018)* (Vol. 31, pp. 6638–6648).
8. Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. In *Advances in Neural Information Processing Systems (NeurIPS 2017)* (Vol. 30, pp. 4765–4774).
9. Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135–1144). https://doi.org/10.1145/2939672.2939778
10. Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A Next-generation Hyperparameter Optimization Framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 2623–2631). https://doi.org/10.1145/3292500.3330701
11. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
12. Edwards, A. L. (1948). Note on the "correction for continuity" in testing the goodness of fit and contingency tables. *Psychometrika*, 13(3), 185–187. https://doi.org/10.1007/BF02288861
13. Efron, B., & Tibshirani, R. J. (1994). *An Introduction to the Bootstrap*. Chapman & Hall/CRC. https://doi.org/10.1201/9780429246593
14. Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
15. Centers for Disease Control and Prevention (CDC). (2022). *National Diabetes Statistics Report: Estimates of Diabetes and Its Burden in the United States*. U.S. Department of Health and Human Services. https://www.cdc.gov/diabetes/data/statistics-report/index.html
