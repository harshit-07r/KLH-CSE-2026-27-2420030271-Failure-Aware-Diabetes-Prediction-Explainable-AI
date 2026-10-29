# Summary of Resolved Inconsistencies and Items for Author Attention

**Audit Status:** All computational, statistical, and architectural defects have been **100% RESOLVED**.  
**Items for Author Attention:** The following items represent external institutional and administrative disclosures that require direct human input prior to final journal submission.

---

## 1. Summary of Defects Successfully Resolved

| # | Defect / Inconsistency | Pre-Audit Status | Post-Audit Status |
|:---:|:---|:---|:---|
| **1** | Table 6 vs Table 2 discrepancy | Discrepancy between M1 (0.4199/0.3402) and Stacking (0.4180/0.4060) | **RESOLVED:** Traced to unweighted vs balanced OOF weighting regimes. Documented in `reports/audit/numerical_consistency_report.md`. |
| **2** | Scientific Macro-F1 claim | Over-claiming highest Macro-F1 across all models | **RESOLVED:** Re-framed honestly around +1.01% accuracy advantage (p < 0.001) and 973 false alarms eliminated, acknowledging Macro-F1 parity (p = 0.224). |
| **3** | Meta-feature dimension ambiguity | Conflicting claims of 24 vs 27 vs 29 vs 50 features | **RESOLVED:** Verified full 50-feature research matrix and streamlined 27-feature dashboard deployment in `docs/supplementary/meta_feature_dictionary.csv`. |
| **4** | SVM classifier labeling | Mislabeled as kernel SVM | **RESOLVED:** Formally designated as `SGDClassifier(loss='modified_huber')` linear margin classifier. |
| **5** | Survey duplicate profile audit | 23,899 corpus duplicates & 6,923 test vector overlap unaddressed | **RESOLVED:** Verified that overlapping survey responses do not inflate generalization error. Sensitivity analysis persisted in `results/final/duplicate_profile_comparison.csv`. |
| **6** | Subject terminology | Clinical 'patients' terminology in non-clinical phone survey | **RESOLVED:** Replaced all occurrences with 'survey respondents / participants'. |
| **7** | External surveillance dataset role | Dataset 2 (`export.csv`) mischaracterized as external validation | **RESOLVED:** Formally designated as macro-level CDC epidemiological trend surveillance. |
| **8** | Figure concordance | 22 figures lacked single authoritative provenance manifest | **RESOLVED:** All 22 figures verified in PNG (300 DPI), SVG, and PDF with source CSVs cataloged in `reports/validation/figure_provenance_manifest.csv`. |

---

## 2. Items Requiring Direct Human Author Input (Administrative Disclosures)

In adherence to scientific ethics and peer-review publishing rules, the automated assistant did not fabricate human institutional disclosures:

1. **Author Details and Affiliations:**
   - File: `docs/MANUSCRIPT_REVISED.md` (Title Page)
   - Action: Replace the generic placeholder text with the actual names, university departments, and email addresses of the student and faculty researchers.
2. **Institutional Review Board (IRB) / Ethics Declaration:**
   - File: `docs/MANUSCRIPT_REVISED.md` (Section on Ethics)
   - Action: If your university provided an IRB reference or waiver certificate for secondary analysis of de-identified CDC BRFSS public data, insert the protocol number.
3. **Funding Acknowledgement:**
   - File: `docs/MANUSCRIPT_REVISED.md` (Acknowledgments)
   - Action: If the research was sponsored by an institutional seed grant, government agency (e.g., DST, ICMR, NIH), or industry sponsor, declare the grant number; otherwise, state that no specific grant funding was received.
4. **Target Journal Selection & Formatting:**
   - Action: Select your preferred target journal (e.g., *IEEE Journal of Biomedical and Health Informatics*, *Elsevier Computers in Biology and Medicine*, or *BMC Medical Informatics and Decision Making*) and import `docs/MANUSCRIPT_REVISED.md` into the journal's official LaTeX or Word template.
