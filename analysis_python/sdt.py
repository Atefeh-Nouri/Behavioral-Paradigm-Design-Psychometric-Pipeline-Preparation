"""
Signal Detection Theory (SDT) Estimation Module.
Implements Hautus (1995) log-linear correction to prevent infinite values
under extreme hit and false-alarm conditions.
"""

from typing import Tuple
import numpy as np
from scipy.stats import norm


def calculate_hautus_sdt(
    hits: int,
    signal_trials: int,
    false_alarms: int,
    noise_trials: int,
    hit_adj: float = 0.5,
    signal_adj: float = 1.0,
    fa_adj: float = 0.5,
    noise_adj: float = 1.0
) -> Tuple[float, float, float]:
    """
    Computes SDT metrics using Hautus (1995) log-linear correction:
    H_adj = (Hits + hit_adj) / (Signal + signal_adj)
    FA_adj = (FA + fa_adj) / (Noise + noise_adj)

    Returns:
        (d_prime, criterion_c, beta)
    """
    h_adj_val = (hits + hit_adj) / (signal_trials + signal_adj)
    fa_adj_val = (false_alarms + fa_adj) / (noise_trials + noise_adj)

    # Probit link: Inverse Standard Normal CDF
    z_hit = float(norm.ppf(h_adj_val))
    z_fa = float(norm.ppf(fa_adj_val))

    d_prime = z_hit - z_fa
    criterion_c = -0.5 * (z_hit + z_fa)
    beta = float(np.exp(d_prime * criterion_c))

    return d_prime, criterion_c, beta
