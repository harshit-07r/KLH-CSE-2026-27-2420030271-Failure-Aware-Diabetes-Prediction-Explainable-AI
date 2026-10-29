# Dataset Dictionary and Preprocessing Protocol

**Primary Dataset:** CDC Behavioral Risk Factor Surveillance System (BRFSS 2015)  
**File Path:** `data/raw/diabetes_012_health_indicators_BRFSS2015.csv`  
**Dimensions:** 253,680 rows × 22 columns (21 predictors + 1 target)  
**Secondary Dataset:** CDC National Health Interview Survey (NHIS 2000–2018)  
**File Path:** `data/raw/export.csv` ($N = 13,889$) — used strictly for macro-surveillance trends.

---

## 1. Target Encoding Specification

| Column Name | Numeric Code | Class Label | Raw Count | Raw Prevalence | Train Count ($N=202,944$) | Test Count ($N=50,736$) |
|:---|:---:|:---|:---:|:---:|:---:|:---:|
| `Diabetes_012` | **0** | No Diabetes | 213,703 | 84.2412% | 170,962 (84.2410%) | 42,741 (84.2419%) |
| `Diabetes_012` | **1** | Prediabetes | 4,631 | 1.8255% | 3,705 (1.8256%) | 926 (1.8251%) |
| `Diabetes_012` | **2** | Diagnosed Diabetes | 35,346 | 13.9333% | 28,277 (13.9334%) | 7,069 (13.9329%) |

---

## 2. Predictor Variable Dictionary (21 Raw Features)

All 21 features contain **zero missing values** ($0$ NaNs across all 253,680 rows):

| Variable Name | Type | Value Range | Missing Values | Encoding / Description |
|:---|:---:|:---:|:---:|:---|
| `HighBP` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Diagnosed High Blood Pressure |
| `HighChol` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Diagnosed High Blood Cholesterol |
| `CholCheck` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Cholesterol check within past 5 years |
| `BMI` | Continuous | 12.0 – 98.0 | 0 (0.0%) | Body Mass Index ($kg/m^2$) |
| `Smoker` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Smoked ≥ 100 cigarettes in lifetime |
| `Stroke` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Diagnosed history of stroke |
| `HeartDiseaseorAttack` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Coronary heart disease or myocardial infarction |
| `PhysActivity` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Any physical activity in past 30 days outside job |
| `Fruits` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Consumes fruit ≥ 1 time per day |
| `Veggies` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Consumes vegetables ≥ 1 time per day |
| `HvyAlcoholConsump` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Heavy alcohol intake (>14 drinks/wk men, >7 women) |
| `AnyHealthcare` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Any health insurance coverage |
| `NoDocbcCost` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Needed to see doctor in past 12 mo but cost prevented |
| `GenHlth` | Ordinal | 1 – 5 | 0 (0.0%) | 1 = Excellent, 2 = Very Good, 3 = Good, 4 = Fair, 5 = Poor |
| `MentHlth` | Discrete | 0 – 30 | 0 (0.0%) | Days of poor mental health in past 30 days |
| `PhysHlth` | Discrete | 0 – 30 | 0 (0.0%) | Days of physical illness or injury in past 30 days |
| `DiffWalk` | Binary | 0, 1 | 0 (0.0%) | 0 = No, 1 = Serious difficulty walking or climbing stairs |
| `Sex` | Binary | 0, 1 | 0 (0.0%) | 0 = Female, 1 = Male |
| `Age` | Ordinal | 1 – 13 | 0 (0.0%) | 5-year age bands: 1 = 18–24, ..., 9 = 60–64, ..., 13 = 80+ |
| `Education` | Ordinal | 1 – 6 | 0 (0.0%) | 1 = None/Kindergarten, ..., 4 = High school grad, ..., 6 = College 4+ |
| `Income` | Ordinal | 1 – 8 | 0 (0.0%) | 1 = <$10k, ..., 5 = <$35k, ..., 8 = ≥$75k |

---

## 3. Preprocessing Protocol

1. **Missing Data:** Confirmed complete case reporting across all 253,680 instances; no imputation was needed or applied.
2. **Duplicate Profiles:** 23,899 duplicate records in raw BRFSS. These represent identical multi-attribute survey responses across distinct respondents in a national phone survey, not patient data duplication.
3. **Feature Scaling:** `StandardScaler` (zero mean, unit variance) fit strictly on the 202,944 training instances.
4. **Resampling:** No synthetic oversampling (SMOTE) was used. Class imbalance was addressed via analytic sample weights (`class_weight='balanced'`).
