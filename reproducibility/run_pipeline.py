import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
preds_path = os.path.join(root, "TEST_PREDICTIONS_MASTER.csv")
benchmark_path = os.path.join(root, "results", "final", "metrics_master.csv")

print("=" * 80)
print("FAILURE-AWARE DIABETES SURVEILLANCE PIPELINE: INDEPENDENT REPRODUCTION RUNNER")
print("=" * 80)

if not os.path.exists(preds_path):
    print(f"Error: {preds_path} not found.")
    sys.exit(1)

df_preds = pd.read_csv(preds_path)
y_true = df_preds["y_true"].values
print(f"Loaded {len(y_true)} locked test set predictions.")

df_bench = pd.read_csv(benchmark_path)
print(f"Loaded {len(df_bench)} authoritative benchmark models from {benchmark_path}.")

models_to_verify = [
    ("Production_Hybrid_Corrected", "Production_Hybrid_Corrected_pred"),
    ("Standard_Stacking_Corrected", "Standard_Stacking_Corrected_pred"),
    ("SVM", "SVM_pred"),
    ("XGBoost", "XGBoost_pred"),
    ("LightGBM", "LightGBM_pred"),
    ("CatBoost", "CatBoost_pred"),
    ("RandomForest", "RandomForest_pred"),
    ("Soft_Voting", "Soft_Voting_pred"),
    ("DecisionTree", "DecisionTree_pred"),
    ("LogisticRegression", "LogisticRegression_pred"),
    ("Standard_Stacking", "Standard_Stacking_pred"),
    ("Production_Hybrid_Original", "Production_Hybrid_Original_pred")
]

all_passed = True
print("\n" + "-" * 80)
print(f"{'Model Configuration':<32} | {'Metric':<12} | {'Computed':<10} | {'Benchmark':<10} | {'Status'}")
print("-" * 80)

for bench_name, col_name in models_to_verify:
    if col_name not in df_preds.columns:
        print(f"Column {col_name} missing from predictions file.")
        all_passed = False
        continue
    
    yp = df_preds[col_name].values
    acc = accuracy_score(y_true, yp)
    mf1 = f1_score(y_true, yp, average="macro", zero_division=0)
    rec1 = np.mean(yp[y_true == 1] == 1)
    
    row_b = df_bench[df_bench["Model"] == bench_name]
    if len(row_b) == 0:
        print(f"Benchmark row for {bench_name} not found.")
        all_passed = False
        continue
    row_b = row_b.iloc[0]
    
    b_acc = row_b["Accuracy"]
    b_mf1 = row_b["Macro_F1"]
    b_rec1 = row_b["Class1_Recall"]
    
    diff_acc = abs(acc - b_acc)
    diff_mf1 = abs(mf1 - b_mf1)
    diff_rec1 = abs(rec1 - b_rec1)
    
    status_acc = "PASS" if diff_acc < 1e-4 else "FAIL"
    status_mf1 = "PASS" if diff_mf1 < 1e-4 else "FAIL"
    status_rec1 = "PASS" if diff_rec1 < 1e-4 else "FAIL"
    
    print(f"{bench_name:<32} | {'Accuracy':<12} | {acc:.6f}   | {b_acc:.6f}   | {status_acc}")
    print(f"{'':<32} | {'Macro-F1':<12} | {mf1:.6f}   | {b_mf1:.6f}   | {status_mf1}")
    print(f"{'':<32} | {'Prediab Rec':<12} | {rec1:.6f}   | {b_rec1:.6f}   | {status_rec1}")
    print("-" * 80)
    
    if status_acc == "FAIL" or status_mf1 == "FAIL" or status_rec1 == "FAIL":
        all_passed = False

if all_passed:
    print("\nREPRODUCIBILITY VERIFICATION OUTCOME: ALL 12 MODELS PASSED WITH 100% CONCORDANCE!")
else:
    print("\nREPRODUCIBILITY VERIFICATION OUTCOME: DISCREPANCIES DETECTED.")
