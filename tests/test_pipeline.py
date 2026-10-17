"""
Pytest Unit Testing Suite for Psychometric Cleaning & Scoring Pipelines.
Tests analytical edge cases: zero false alarms, boundary extremes, adversarial MAD inputs.
"""

import os
import sys
import numpy as np
import pandas as pd
import pytest
from scipy.stats import norm

try:
    from analysis_python.clean import compute_within_subject_mad_bounds, flag_trial_anomalies
    from analysis_python.sdt import calculate_hautus_sdt
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from analysis_python.clean import compute_within_subject_mad_bounds, flag_trial_anomalies
    from analysis_python.sdt import calculate_hautus_sdt


def test_sdt_zero_false_alarms():
    """Confirms Hautus correction handles zero false alarms without returning infinite d'."""
    d_prime, c, beta = calculate_hautus_sdt(hits=70, signal_trials=70, false_alarms=0, noise_trials=30)

    # Hand-computed targets with Hautus adjustment
    h_adj = (70 + 0.5) / (70 + 1.0)  # 70.5 / 71.0 = 0.9929577
    fa_adj = (0 + 0.5) / (30 + 1.0)   # 0.5 / 31.0 = 0.0161290
    expected_d = norm.ppf(h_adj) - norm.ppf(fa_adj)
    expected_c = -0.5 * (norm.ppf(h_adj) + norm.ppf(fa_adj))

    assert np.isfinite(d_prime)
    assert np.isfinite(c)
    assert abs(d_prime - expected_d) < 1e-6
    assert abs(c - expected_c) < 1e-6


def test_sdt_zero_hits():
    """Confirms Hautus correction handles zero hits without returning -inf."""
    d_prime, c, beta = calculate_hautus_sdt(hits=0, signal_trials=70, false_alarms=10, noise_trials=30)
    assert np.isfinite(d_prime)
    assert d_prime < 0.0  # Performance below chance


def test_mad_filtering_identical_values():
    """Confirms MAD filter handles identical RTs (MAD = 0) without dividing by zero.

    When all RTs are identical, MAD == 0, so the raw bounds
    (median +/- k*MAD) collapse to the median itself:
        lower = max(150.0, 400.0 - 3*0) = max(150.0, 400.0) = 400.0
        upper = min(2000.0, 400.0 + 3*0) = min(2000.0, 400.0) = 400.0

    Contract invariants under test:
      1. No ZeroDivisionError (MAD == 0 must not cause failure).
      2. low_b <= high_b always holds.
      3. All 400s remain in-bounds (no value falsely flagged as outlier).
    """
    dummy_df = pd.DataFrame({"rt_ms": [400.0] * 50})
    low_b, high_b = compute_within_subject_mad_bounds(dummy_df, k=3.0)

    assert low_b == 400.0, f"Expected degenerate lower bound 400.0, got {low_b}"
    assert high_b == 400.0, f"Expected degenerate upper bound 400.0, got {high_b}"
    assert low_b <= high_b, "lower_bound must never exceed upper_bound"


def test_mad_filtering_extreme_outlier():
    """Confirms single extreme outliers are cleanly bounded."""
    normal_rts = list(np.random.normal(400.0, 20.0, 99))
    normal_rts.append(1999.0)  # Severe lapse outlier
    dummy_df = pd.DataFrame({"rt_ms": normal_rts})

    low_b, high_b = compute_within_subject_mad_bounds(dummy_df, k=3.0)
    assert high_b < 600.0  # High bound should remain close to central tendency


def test_no_silent_drops():
    """Confirms trial count is preserved when flagging anomalies."""
    config = {
        "cleaning_rules": {
            "rt_cutoffs_ms": {"min": 150.0, "max": 2000.0},
            "mad_filtering": {"threshold_k": 3.0, "scale_constant": 1.4826022185056}
        }
    }
    dummy_trials = pd.DataFrame({
        "participant_id": ["P1"] * 10,
        "trial_type": ["AX"] * 10,
        "is_correct": [True] * 10,
        "outcome_code": ["HIT"] * 10,
        "flag_duplicate_row": [False] * 10,
        "rt_ms": [100.0, 350.0, 360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 2500.0]
    })

    flagged_df = flag_trial_anomalies(dummy_trials, config)
    assert len(flagged_df) == 10  # Row count preserved
    assert flagged_df.loc[0, "flag_anticipation"] == True  # 100ms flagged as anticipation
    assert flagged_df.loc[9, "flag_absolute_outlier"] == True  # 2500ms flagged as absolute outlier
    assert flagged_df["is_retained_for_rt"].sum() == 8  # Middle 8 retained
