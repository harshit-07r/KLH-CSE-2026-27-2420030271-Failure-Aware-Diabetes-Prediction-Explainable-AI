# Three-Class Diabetes Status Classification: Reproducibility Package

This package contains full environment specifications, seed registries, data dictionaries, and an independent reproduction script for the research paper:

**"Evaluating Failure-Aware Ensemble Learning and Explainable AI for Three-Class Diabetes Status Classification: Analysis of CDC BRFSS Surveillance Data"**

---

## 1. Quick Reproduction (30 Seconds)

To independently verify that all multi-class metrics, confusion matrices, and model evaluations match the authoritative benchmark results persisted in `results/final/metrics_master.csv`:

```powershell
python reproducibility/run_pipeline.py
```

Expected output:
- `10 / 10 models evaluated`
- `Accuracy, Macro-F1, and Prediabetes Recall concordant within 10^-6 tolerance`
- `REPRODUCIBILITY VERIFICATION OUTCOME: ALL TESTS PASSED WITH 100% CONCORDANCE!`

---

## 2. Conda Environment Setup

To recreate the exact Python execution environment:

```powershell
conda env create -f reproducibility/environment.yml
conda activate diabetes_surveillance
```

Alternatively, with pip:

```powershell
pip install -r reproducibility/requirements.txt
```

---

## 3. Package File Directory

- `requirements.txt`: Pinned Python dependencies.
- `environment.yml`: Conda environment specification.
- `seed_registry.json`: Machine-readable random seed definitions for all algorithms and bootstrap resamples.
- `dataset_dictionary.md`: Detailed specification of BRFSS 2015 and NHIS data variables, encodings, and preprocessing.
- `run_pipeline.py`: Independent automated reproduction test script.
