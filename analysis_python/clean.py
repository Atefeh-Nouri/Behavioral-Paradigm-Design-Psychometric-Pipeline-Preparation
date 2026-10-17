"""
Psychometric Cleaning and Non-Destructive Outlier Flagging Engine.
Implements within-subject Median Absolute Deviation (MAD) latency filtering.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


def compute_within_subject_mad_bounds(
    df_subject_ax: pd.DataFrame,
    k: float = 3.0,
    scale_constant: float = 1.4826022185056
) -> Tuple[float, float]:
    """
    Calculates non-parametric outlier boundaries using Median Absolute Deviation (MAD):
    MAD = scale_constant * median(|x - median(x)|)
    Bounds = [max(min_rt, median - k * MAD), min(max_rt, median + k * MAD)]
    """
    valid_rts = df_subject_ax.loc[df_subject_ax["rt_ms"].notna(), "rt_ms"].values
    if len(valid_rts) == 0:
        return 150.0, 2000.0

    med = float(np.median(valid_rts))
    mad = float(scale_constant * np.median(np.abs(valid_rts - med)))

    lower_bound = max(150.0, med - (k * mad))
    upper_bound = min(2000.0, med + (k * mad))
    return lower_bound, upper_bound


def flag_trial_anomalies(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Decorates the trial DataFrame with non-destructive audit flags.
    No rows are deleted, preserving full trial geometry.
    """
    df = df.copy()
    clean_cfg = config["cleaning_rules"]
    min_rt = clean_cfg["rt_cutoffs_ms"]["min"]
    max_rt = clean_cfg["rt_cutoffs_ms"]["max"]
    k_mad = clean_cfg["mad_filtering"]["threshold_k"]
    scale_c = clean_cfg["mad_filtering"]["scale_constant"]

    # 1. Base Latency Flags
    df["flag_missing_rt"] = df["rt_ms"].isna()
    df["flag_anticipation"] = df["rt_ms"].notna() & (df["rt_ms"] < min_rt)
    df["flag_timeout_lapse"] = df["flag_missing_rt"] | (df["rt_ms"] > 1000.0)
    df["flag_absolute_outlier"] = df["rt_ms"].notna() & ((df["rt_ms"] < min_rt) | (df["rt_ms"] > max_rt))
    df["flag_mad_outlier"] = False

    # 2. Within-Subject MAD Outlier Flagging on Correct AX Trials
    for subj_id, subj_group in df.groupby("participant_id"):
        ax_correct = subj_group[
            (subj_group["trial_type"] == "AX") &
            (subj_group["is_correct"]) &
            (~subj_group["flag_anticipation"]) &
            (~subj_group["flag_duplicate_row"])
        ]

        low_b, high_b = compute_within_subject_mad_bounds(ax_correct, k=k_mad, scale_constant=scale_c)

        # Mask outliers across this subject's trials
        subj_mask = (df["participant_id"] == subj_id) & df["rt_ms"].notna()
        outlier_mask = subj_mask & ((df["rt_ms"] < low_b) | (df["rt_ms"] > high_b))
        df.loc[outlier_mask, "flag_mad_outlier"] = True

    # 3. Inclusion Gates
    df["is_retained_for_rt"] = (
        df["is_correct"] &
        (~df["flag_duplicate_row"]) &
        (~df["flag_absolute_outlier"]) &
        (~df["flag_mad_outlier"])
    )

    df["is_retained_for_sdt"] = (
        (~df["flag_duplicate_row"]) &
        (~df["flag_anticipation"])
    )

    return df
