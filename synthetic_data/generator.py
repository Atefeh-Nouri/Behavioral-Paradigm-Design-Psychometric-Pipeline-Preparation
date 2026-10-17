"""
Hierarchical Synthetic Behavioral Data Generator for AX-CPT.
Produces synthetic trial records conforming to Raw Data Schema v1.0.
"""

from dataclasses import dataclass
import random
from typing import Any, Dict, List, Optional, Tuple
import uuid
import numpy as np
import pandas as pd


@dataclass
class SubjectTraits:
    """Individual latent traits drawn from population priors."""
    subject_id: str
    mu: float
    sigma: float
    tau: float
    d_prime: float
    criterion: float
    beta_mu: float
    beta_tau: float
    pes_ms: float
    p_anticipation: float
    p_omission: float
    is_stress_case: bool = False


class SyntheticDataGenerator:
    """
    Config-driven, hierarchical generator simulating cognitive dynamics,
    distributional RT skew, and decision accuracy.
    """
    def __init__(self, config: dict, master_seed: int = 42):
        self.config = config
        self.master_seed = master_seed
        self.rng_master = np.random.default_rng(master_seed)

    def draw_subject_traits(self, subject_id: str, is_stress_case: bool = False) -> SubjectTraits:
        """Samples subject-level traits from hierarchical population distributions."""
        if is_stress_case:
            # Stress-test case: Near-chance discriminability, extreme lapses, high omissions
            return SubjectTraits(
                subject_id=subject_id,
                mu=460.0,
                sigma=75.0,
                tau=320.0,
                d_prime=0.20,
                criterion=0.10,
                beta_mu=50.0,
                beta_tau=60.0,
                pes_ms=10.0,
                p_anticipation=0.08,
                p_omission=0.18,
                is_stress_case=True
            )

        # Standard healthy population sampling
        mu = float(self.rng_master.normal(380.0, 35.0))
        sigma = float(np.clip(self.rng_master.normal(42.0, 8.0), 15.0, 80.0))

        # Gamma-distributed tau to prevent non-positive lapse scales
        alpha_tau = (85.0 ** 2) / (22.0 ** 2)
        beta_tau = 85.0 / (22.0 ** 2)
        tau = float(self.rng_master.gamma(alpha_tau, 1.0 / beta_tau))

        # Correlated d' and criterion
        cov_matrix = [[0.45**2, -0.30 * 0.45 * 0.25], [-0.30 * 0.45 * 0.25, 0.25**2]]
        d_val, c_val = self.rng_master.multivariate_normal([3.40, 1.10], cov_matrix)

        return SubjectTraits(
            subject_id=subject_id,
            mu=mu,
            sigma=sigma,
            tau=tau,
            d_prime=float(np.clip(d_val, 1.5, 4.8)),
            criterion=float(np.clip(c_val, 0.2, 2.0)),
            beta_mu=float(self.rng_master.normal(30.0, 10.0)),
            beta_tau=float(self.rng_master.normal(25.0, 8.0)),
            pes_ms=float(self.rng_master.normal(35.0, 12.0)),
            p_anticipation=float(self.rng_master.beta(1.5, 98.5)),
            p_omission=float(self.rng_master.beta(1.0, 99.0)),
            is_stress_case=False
        )

    def simulate_trial(
        self,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Simulates response latency and outcome for a single trial."""
        # Handle both signature orders flexibly
        if len(args) == 4:
            if isinstance(args[0], dict):
                trial_def, trial_idx, is_post_error, traits = args
                rng = kwargs.get('rng', getattr(self, 'rng_master', None))
            else:
                traits, trial_def, trial_idx, is_post_error = args
                rng = kwargs.get('rng', getattr(self, 'rng_master', None))
        elif len(args) >= 5:
            traits, trial_def, trial_idx, is_post_error, rng = args[:5]
        else:
            trial_def = kwargs.get('trial_def') or kwargs.get('t_dict') or (args[0] if len(args) > 0 and isinstance(args[0], dict) else args[1] if len(args) > 1 else None)
            trial_idx = kwargs.get('trial_idx') or kwargs.get('global_idx') or (args[1] if len(args) > 1 and isinstance(args[1], int) else args[2] if len(args) > 2 else 0)
            is_post_error = kwargs.get('is_post_error', False)
            traits = kwargs.get('traits') or (args[0] if len(args) > 0 and not isinstance(args[0], dict) else args[3] if len(args) > 3 else None)
            rng = kwargs.get('rng', getattr(self, 'rng_master', None))
        if rng is None:
            rng = getattr(self, 'rng_master', None)
        t_type = trial_def["trial_type"]
        delay_cond = trial_def["block_condition"]

        # 1. Evaluate Anticipation
        if rng.random() < traits.p_anticipation:
            rt_ms = float(rng.uniform(60.0, 145.0))
            resp_key = rng.choice(["space", "l"])
            is_correct = (resp_key == trial_def["required_key"])
            return self._build_record(trial_def, trial_idx, rt_ms, resp_key, is_correct, "ANTICIPATION", True, is_post_error)

        # 2. Evaluate Baseline Omission
        if rng.random() < traits.p_omission:
            return self._build_record(trial_def, trial_idx, None, None, False, "OMISSION_ERROR", False, is_post_error)

        # 3. Compute Shifted Ex-Gaussian Parameters
        mu_shift = 0.0
        tau_shift = 0.0

        if t_type == "AY":
            mu_shift += 65.0  # Conflict interference slowing
        elif t_type == "BX":
            mu_shift += 20.0
            if delay_cond == "LONG_DELAY":
                tau_shift += 35.0  # Context maintenance failure lapse

        if is_post_error:
            mu_shift += traits.pes_ms  # Post-error slowing

        # Time-on-task vigilance drift across the 400 trials
        time_factor = trial_idx / 400.0
        mu_trial = traits.mu + mu_shift + (traits.beta_mu * time_factor)
        tau_trial = traits.tau + tau_shift + (traits.beta_tau * time_factor)
        sigma_trial = traits.sigma + (15.0 if t_type == "AY" else 0.0)

        # Sample Latency via Independent Convolution: Normal + Exponential
        gaussian_component = rng.normal(mu_trial, sigma_trial)
        exponential_component = rng.exponential(tau_trial)
        rt_ms = float(gaussian_component + exponential_component)

        # 4. Check for Timeout Lapses
        if rt_ms > self.config["timing"]["response_window_ms"]:
            return self._build_record(trial_def, trial_idx, None, None, False, "OMISSION_ERROR", False, is_post_error)

        # 5. Signal Detection Decision Logic
        if t_type == "AX":
            delta_e = traits.d_prime
        elif t_type == "AY":
            delta_e = 0.50 * traits.d_prime
        elif t_type == "BX":
            delta_e = 0.15 * traits.d_prime + (0.60 if delay_cond == "LONG_DELAY" else 0.0)
        else:  # BY
            delta_e = 0.0

        evidence = rng.normal(delta_e, 1.0)
        is_target_response = (evidence > traits.criterion)
        resp_key = "space" if is_target_response else "l"
        is_correct = (resp_key == trial_def["required_key"])

        # Determine outcome code
        if resp_key == trial_def["required_key"]:
            outcome = "HIT" if t_type == "AX" else "CORRECT_REJECTION"
        else:
            outcome = "COMMISSION_ERROR"

        return self._build_record(trial_def, trial_idx, rt_ms, resp_key, is_correct, outcome, False, is_post_error)

    def _build_record(
        self,
        t_def: dict,
        trial_idx: int,
        rt_ms: Optional[float],
        resp_key: Optional[str],
        is_correct: bool,
        outcome: str,
        is_anticipation: bool,
        is_post_error: bool
    ) -> Dict[str, Any]:
        """Maps trial outcome directly to Raw Data Schema v1.0."""
        return {
            "session_id": t_def["session_id"],
            "participant_id": t_def["participant_id"],
            "block_index": t_def["block_index"],
            "block_condition": t_def["block_condition"],
            "trial_index_global": trial_idx,
            "trial_index_block": t_def["trial_index_block"],
            "trial_type": t_def["trial_type"],
            "cue_stimulus": t_def["cue_stimulus"],
            "probe_stimulus": t_def["probe_stimulus"],
            "required_key": t_def["required_key"],
            "cpi_nominal_ms": float(t_def["cpi_nominal_ms"]),
            "cpi_realized_ms": float(t_def["cpi_nominal_ms"] + np.random.normal(0.0, 0.4)),
            "fixation_realized_ms": float(500.0 + np.random.uniform(-95.0, 95.0)),
            "probe_onset_timestamp": round(10.0 + (trial_idx * 4.2), 5),
            "response_key": resp_key,
            "response_timestamp": round(10.0 + (trial_idx * 4.2) + (rt_ms / 1000.0), 5) if rt_ms else None,
            "rt_ms": round(rt_ms, 3) if rt_ms is not None else None,
            "is_correct": bool(is_correct),
            "outcome_code": outcome,
            "is_anticipation": bool(is_anticipation),
            "post_error_trial": bool(is_post_error),
            "frame_drop_detected": False
        }


def inject_dataset_anomalies(df: pd.DataFrame, subject_id: str, rng: np.random.Generator) -> pd.DataFrame:
    """
    Applies configurable technical anomalies to a completed session DataFrame:
    1. Row deletions (simulating packet drops).
    2. Row duplications (simulating retry loops).
    3. Clock corruptions (negative or out-of-range RTs).
    """
    records = df.copy()

    # 1. Missing Rows (0.5% rate)
    drop_indices = rng.choice(records.index, size=int(len(records) * 0.005), replace=False)
    records = records.drop(drop_indices)

    # 2. Duplicated Rows (0.25% rate)
    dup_indices = rng.choice(records.index, size=int(len(records) * 0.0025), replace=False)
    dup_rows = records.loc[dup_indices].copy()
    records = pd.concat([records, dup_rows]).sort_values("trial_index_global").reset_index(drop=True)

    # 3. Corrupt Clock Readings (0.25% rate)
    corrupt_indices = rng.choice(records.index, size=int(len(records) * 0.0025), replace=False)
    for idx in corrupt_indices:
        if records.loc[idx, "rt_ms"] is not None:
            # Inject either negative latency or unphysiologically high latency
            records.loc[idx, "rt_ms"] = float(rng.choice([-99.0, 14205.0]))

    return records
