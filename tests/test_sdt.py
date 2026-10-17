"""
Analytical Signal Detection Theory (SDT) Hand-Calculated Test Cases (Amendment 3).
Asserts exact mathematical recovery of d', criterion c, and beta under Hautus (1995)
log-linear adjustments, specifically testing 0/1 rate boundaries and neutral symmetry.
"""

import math
import os
import sys
import numpy as np
import pytest
from scipy.stats import norm

try:
    from analysis_python.sdt import calculate_hautus_sdt
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from analysis_python.sdt import calculate_hautus_sdt


def test_sdt_hand_computed_perfect_boundary():
    """
    Test Case 1: Ceiling Performance (100% Hits, 0% False Alarms)
    Signal: 70 trials, 70 Hits
    Noise:  30 trials,  0 False Alarms

    Hautus Adjustment:
      H_adj  = (70 + 0.5) / (70 + 1.0) = 70.5 / 71.0 = 0.9929577465
      FA_adj = ( 0 + 0.5) / (30 + 1.0) =  0.5 / 31.0 = 0.0161290323

      z_hit  = norm.ppf(0.9929577465) = 2.4553255
      z_fa   = norm.ppf(0.0161290323) = -2.1413847

      d' = z_hit - z_fa = 2.4553255 - (-2.1413847) = 4.5967102
      c  = -0.5 * (z_hit + z_fa) = -0.1569704
    """
    d_prime, c, beta = calculate_hautus_sdt(hits=70, signal_trials=70, false_alarms=0, noise_trials=30)

    expected_h_adj = 70.5 / 71.0
    expected_fa_adj = 0.5 / 31.0
    expected_z_hit = norm.ppf(expected_h_adj)
    expected_z_fa = norm.ppf(expected_fa_adj)
    expected_d = expected_z_hit - expected_z_fa
    expected_c = -0.5 * (expected_z_hit + expected_z_fa)

    assert np.isfinite(d_prime)
    assert np.isfinite(c)
    assert abs(d_prime - expected_d) < 1e-6
    assert abs(c - expected_c) < 1e-6
    assert d_prime > 4.5  # High discriminability cleanly resolved


def test_sdt_hand_computed_floor_boundary():
    """
    Test Case 2: Inverted Performance (0% Hits, 100% False Alarms)
    Signal: 70 trials,  0 Hits
    Noise:  30 trials, 30 False Alarms
    """
    d_prime, c, beta = calculate_hautus_sdt(hits=0, signal_trials=70, false_alarms=30, noise_trials=30)

    expected_h_adj = 0.5 / 71.0
    expected_fa_adj = 30.5 / 31.0
    expected_d = norm.ppf(expected_h_adj) - norm.ppf(expected_fa_adj)
    expected_c = -0.5 * (norm.ppf(expected_h_adj) + norm.ppf(expected_fa_adj))

    assert np.isfinite(d_prime)
    assert d_prime < -4.5
    assert abs(d_prime - expected_d) < 1e-6
    assert abs(c - expected_c) < 1e-6


def test_sdt_neutral_chance_symmetry():
    """
    Test Case 3: Exactly Balanced Chance Response (50% Hit rate, 50% FA rate)
    Signal: 100 trials, 50 Hits
    Noise:  100 trials, 50 False Alarms

    H_adj  = (50 + 0.5) / (100 + 1.0) = 50.5 / 101.0 = 0.50
    FA_adj = (50 + 0.5) / (100 + 1.0) = 50.5 / 101.0 = 0.50
    z_hit = 0.0, z_fa = 0.0 -> d' = 0.0, c = 0.0, beta = 1.0
    """
    d_prime, c, beta = calculate_hautus_sdt(hits=50, signal_trials=100, false_alarms=50, noise_trials=100)

    assert abs(d_prime - 0.0) < 1e-6
    assert abs(c - 0.0) < 1e-6
    assert abs(beta - 1.0) < 1e-6


def test_sdt_conservative_vs_liberal_shifts():
    """
    Test Case 4: Verifies directionality of decision criterion c:
    - Conservative bias (withholds responses -> low Hits, low FAs) -> c > 0
    - Liberal bias (presses freely -> high Hits, high FAs) -> c < 0
    """
    # Conservative observer: 30% hits (30/100), 5% FAs (5/100)
    d_cons, c_cons, _ = calculate_hautus_sdt(hits=30, signal_trials=100, false_alarms=5, noise_trials=100)
    assert c_cons > 0.5  # Conservative criterion is positive

    # Liberal observer: 95% hits (95/100), 70% FAs (70/100)
    d_lib, c_lib, _ = calculate_hautus_sdt(hits=95, signal_trials=100, false_alarms=70, noise_trials=100)
    assert c_lib < -0.5  # Liberal criterion is negative
