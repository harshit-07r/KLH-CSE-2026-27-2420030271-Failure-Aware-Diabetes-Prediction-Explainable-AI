# Scholarly References and Author Declarations Requiring Human Review

**Audit Objective:** Strict Scholarly Verification & DOI Audit  
**Auditor:** Antigravity Scholarly Integrity Verification Group  
**Date:** 2026-10-29  
**Policy:** **STRICT ZERO HALLUCINATION POLICY** — All 15 foundational machine learning, clinical, and statistical citations were verified via official repositories (Crossref, ACM, NeurIPS, Springer, CDC). Two institutional declarations require human author input prior to journal submission.

---

## 1. Verified Genuine References (15/15 Pass)

All 15 scholarly references in `reports/audit/reference_verification.csv` were verified with active, genuine DOIs and URLs:
1. **CDC (2016):** BRFSS 2015 Survey Data and Documentation.
2. **American Diabetes Association (2024):** Classification and Diagnosis of Diabetes (DOI: `10.2337/dc24-S002`).
3. **Wolpert (1992):** Stacked Generalization (DOI: `10.1016/S0893-6080(05)80023-1`).
4. **Breiman (2001):** Random Forests (DOI: `10.1023/A:1010933404324`).
5. **Chen & Guestrin (2016):** XGBoost (DOI: `10.1145/2939672.2939785`).
6. **Ke et al. (2017):** LightGBM (NeurIPS 2017).
7. **Prokhorenkova et al. (2018):** CatBoost (NeurIPS 2018).
8. **Lundberg & Lee (2017):** A Unified Approach to Interpreting Model Predictions (NeurIPS 2017, SHAP).
9. **Ribeiro et al. (2016):** "Why Should I Trust You?": Explaining the Predictions of Any Classifier (DOI: `10.1145/2939672.2939778`, LIME).
10. **Akiba et al. (2019):** Optuna (DOI: `10.1145/3292500.3330701`).
11. **Pedregosa et al. (2011):** Scikit-learn (JMLR 2011).
12. **Edwards (1948):** Correction for Continuity in Contingency Tables (DOI: `10.1007/BF02288861`).
13. **Efron & Tibshirani (1994):** An Introduction to the Bootstrap (DOI: `10.1201/9780429246593`).
14. **Brier (1950):** Verification of forecasts in terms of probability (DOI: `10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2`).
15. **CDC (2022):** National Diabetes Statistics Report.

---

## 2. Declarations Requiring Direct Human Author Input (2 Items)

In strict compliance with peer-review publication standards, the AI assistant **did not guess, synthesize, or invent** institutional, author, or ethical identifiers:

### Item 1: Institutional Review Board (IRB) / Ethics Approval Statement
- **Current Status:** Placeholder in manuscript acknowledgments.
- **Author Action Required:** State whether this research was conducted under a specific Institutional Review Board protocol number (e.g., from your university/institute) or whether it qualifies for an Institutional Exemption certificate because CDC BRFSS public-use data is completely de-identified and publicly available.
- **Suggested Text if Exempt:**  
  *"Ethical Approval: The analysis utilized public-use, de-identified surveillance data provided by the Centers for Disease Control and Prevention (CDC). In accordance with U.S. Federal Policy for the Protection of Human Subjects (45 CFR 46), secondary analysis of publicly available, de-identified data does not constitute human subjects research and is exempt from formal institutional review."*

### Item 2: Funding and Conflict of Interest Declaration
- **Current Status:** Placeholder.
- **Author Action Required:** Insert any university internal funding grant, agency sponsorship (e.g., DST, ICMR, NIH, or university research seed grant), or state:  
  *"Funding: This research received no external grant funding. Conflicts of Interest: The authors declare that they have no competing financial or personal interests."*

### Item 3: Author Affiliation and Email Addresses
- **Author Action Required:** Populate the final title page author block with the exact names, institutional department affiliations, and corresponding author email addresses of the research team.
