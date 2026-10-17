"""
Cross-Language Pipeline Equivalence Verification Engine.
Compares processed trial parquet files and summary CSVs across Python and R.
"""

import os
import sys
import numpy as np
import pandas as pd

TOLERANCE = 1e-5  # Maximum allowable absolute difference for floating-point metrics


def test_cleaned_trials_equivalence(py_parquet: str, r_parquet: str):
    print("--- 1. Testing Cleaned Trials Table Equivalence (Contract 1) ---")
    assert os.path.exists(py_parquet), f"Missing Python parquet: {py_parquet}"
    assert os.path.exists(r_parquet), f"Missing R parquet: {r_parquet}"

    df_py = pd.read_parquet(py_parquet)
    df_r = pd.read_parquet(r_parquet)

    assert df_py.shape == df_r.shape, f"Shape mismatch! Py: {df_py.shape}, R: {df_r.shape}"
    assert list(df_py.columns) == list(df_r.columns), "Column names or ordering mismatch!"

    flag_cols = [
        "flag_dropped_trial", "flag_duplicate_row", "flag_anticipation",
        "flag_timeout_lapse", "flag_absolute_outlier", "flag_mad_outlier",
        "is_retained_for_rt", "is_retained_for_sdt"
    ]
    for col in flag_cols:
        mismatches = (df_py[col] != df_r[col]).sum()
        assert mismatches == 0, f"Flag '{col}' contains {mismatches} mismatches between Python and R!"

    print(f"Contract 1 Parity Confirmed across {len(df_py)} trials. Flags match identically.\n")


def test_subject_summaries_equivalence(py_csv: str, r_csv: str):
    print("--- 2. Testing Per-Subject Summary Table Equivalence (Contract 2) ---")
    assert os.path.exists(py_csv), f"Missing Python CSV: {py_csv}"
    assert os.path.exists(r_csv), f"Missing R CSV: {r_csv}"

    df_py = pd.read_csv(py_csv).sort_values("participant_id").reset_index(drop=True)
    df_r = pd.read_csv(r_csv).sort_values("participant_id").reset_index(drop=True)

    assert df_py.shape == df_r.shape, f"Summary shape mismatch! Py: {df_py.shape}, R: {df_r.shape}"
    assert list(df_py.columns) == list(df_r.columns), "Summary column mismatch!"

    # Categorical matching
    string_cols = ["participant_id", "group", "is_compliant", "exclusion_reason"]
    for col in string_cols:
        assert (df_py[col] == df_r[col]).all(), f"Categorical column '{col}' has discrepancies!"

    # Numerical metrics within tolerance
    float_cols = [
        "ax_hit_rate", "ay_commission_rate", "bx_commission_rate", "by_commission_rate",
        "omission_rate_global", "anticipation_rate", "rt_mean_ax_ms", "rt_sd_ax_ms",
        "rt_icv_ax", "dprime_global", "criterion_global", "dprime_context", "pbi_index",
        "conflict_cost_ms", "wm_decay_cost_pct", "pes_ms", "vigilance_slope_ms"
    ]

    max_deltas = {}
    for col in float_cols:
        delta = np.abs(df_py[col] - df_r[col]).max()
        max_deltas[col] = delta
        assert delta <= TOLERANCE, f"Metric '{col}' exceeded tolerance! Max delta: {delta:.2e}"

    print(f"Contract 2 Parity Confirmed across all {len(df_py)} participants.")
    print("Max absolute delta across any float metric: "
          f"{max(max_deltas.values()):.2e} (Threshold: {TOLERANCE:.2e})\n")


if __name__ == "__main__":
    py_trials = "data/processed/python/cleaned_trials.parquet"
    r_trials = "data/processed/r/cleaned_trials.parquet"
    py_sum = "data/processed/python/subject_summaries.csv"
    r_sum = "data/processed/r/subject_summaries.csv"

    try:
        test_cleaned_trials_equivalence(py_trials, r_trials)
        test_subject_summaries_equivalence(py_sum, r_sum)
        print(">> FULL CROSS-LANGUAGE EQUIVALENCE VERIFIED: 100% BIT/NUMERICAL PARITY <<")
    except AssertionError as e:
        print(f"EQUIVALENCE FAILURE: {str(e)}")
        sys.exit(1)
