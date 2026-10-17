"""
Subject-Level Psychometric Aggregator.
Consolidates cleaned trial dynamics into Data Contract 2 summary records.
"""

from typing import Any, Dict
import numpy as np
import pandas as pd

try:
    from sdt import calculate_hautus_sdt
except ImportError:
    from .sdt import calculate_hautus_sdt


def summarize_subject_session(
    subj_df: pd.DataFrame,
    is_compliant: bool,
    rejection_reason: str
) -> Dict[str, Any]:
    """Computes all 24 summary metrics for a single participant conforming to Data Contract 2."""
    subj_id = str(subj_df["participant_id"].iloc[0])

    # Extract subject numeric index to recover counterbalancing group
    subj_nr = int("".join(filter(str.isdigit, subj_id)))
    group_val = "A" if (subj_nr % 2 == 1) else "B"

    # Filter trial sets
    valid_sdt = subj_df[subj_df["is_retained_for_sdt"]]
    ax_trials = valid_sdt[valid_sdt["trial_type"] == "AX"]
    ay_trials = valid_sdt[valid_sdt["trial_type"] == "AY"]
    bx_trials = valid_sdt[valid_sdt["trial_type"] == "BX"]
    by_trials = valid_sdt[valid_sdt["trial_type"] == "BY"]

    # 1. Behavioral Response Rates
    ax_hits = int((ax_trials["outcome_code"] == "HIT").sum())
    ax_total = len(ax_trials)
    ax_hit_rate = ax_hits / ax_total if ax_total > 0 else 0.0

    ay_comm = int((ay_trials["outcome_code"] == "COMMISSION_ERROR").sum())
    ay_rate = ay_comm / len(ay_trials) if len(ay_trials) > 0 else 0.0

    bx_comm = int((bx_trials["outcome_code"] == "COMMISSION_ERROR").sum())
    bx_rate = bx_comm / len(bx_trials) if len(bx_trials) > 0 else 0.0

    by_comm = int((by_trials["outcome_code"] == "COMMISSION_ERROR").sum())
    by_rate = by_comm / len(by_trials) if len(by_trials) > 0 else 0.0

    omissions = int((subj_df["outcome_code"] == "OMISSION_ERROR").sum())
    omission_rate = omissions / len(subj_df) if len(subj_df) > 0 else 0.0

    anticipations = int(subj_df["flag_anticipation"].sum())
    anticipation_rate = anticipations / len(subj_df) if len(subj_df) > 0 else 0.0

    # 2. RT Distribution Metrics on Retained AX Trials (ddof=1)
    retained_ax = subj_df[(subj_df["trial_type"] == "AX") & (subj_df["is_retained_for_rt"])]
    rt_vals = retained_ax["rt_ms"].values

    if len(rt_vals) > 1:
        rt_mean = float(np.mean(rt_vals))
        rt_sd = float(np.std(rt_vals, ddof=1))
        rt_icv = rt_sd / rt_mean if rt_mean > 0 else 0.0
    else:
        rt_mean, rt_sd, rt_icv = 0.0, 0.0, 0.0

    # 3. SDT Computations (Hautus log-linear)
    all_noise = len(ay_trials) + len(bx_trials) + len(by_trials)
    all_fa = ay_comm + bx_comm + by_comm
    dp_glob, crit_glob, _ = calculate_hautus_sdt(ax_hits, ax_total, all_fa, all_noise)
    dp_ctx, _, _ = calculate_hautus_sdt(ax_hits, ax_total, bx_comm, len(bx_trials))

    # 4. Proactive Behavioral Index (PBI)
    pbi = (ay_rate - bx_rate) / (ay_rate + bx_rate) if (ay_rate + bx_rate) > 0 else 0.0

    # 5. Contrast Costs
    ay_correct_rt = subj_df[
        (subj_df["trial_type"] == "AY") &
        (subj_df["outcome_code"] == "CORRECT_REJECTION") &
        (subj_df["is_retained_for_rt"])
    ]["rt_ms"].values

    conflict_cost = float(np.mean(ay_correct_rt) - rt_mean) if len(ay_correct_rt) > 0 else 0.0

    # Working Memory Delay Degradation on BX Commission Rate
    bx_short = valid_sdt[(valid_sdt["trial_type"] == "BX") & (valid_sdt["block_condition"] == "SHORT_DELAY")]
    bx_long = valid_sdt[(valid_sdt["trial_type"] == "BX") & (valid_sdt["block_condition"] == "LONG_DELAY")]

    bx_short_err = (bx_short["outcome_code"] == "COMMISSION_ERROR").sum() / len(bx_short) if len(bx_short) > 0 else 0.0
    bx_long_err = (bx_long["outcome_code"] == "COMMISSION_ERROR").sum() / len(bx_long) if len(bx_long) > 0 else 0.0
    wm_decay_cost = float((bx_long_err - bx_short_err) * 100.0)

    # 6. Post-Error Slowing (PES)
    post_error_rts = retained_ax[retained_ax["post_error_trial"]]["rt_ms"].values
    post_correct_rts = retained_ax[~retained_ax["post_error_trial"]]["rt_ms"].values

    if len(post_error_rts) > 0 and len(post_correct_rts) > 0:
        pes = float(np.mean(post_error_rts) - np.mean(post_correct_rts))
    else:
        pes = 0.0

    # 7. Time-on-Task Vigilance Slope (Linear fit of AX RT over blocks 1-4)
    block_means = retained_ax.groupby("block_index")["rt_ms"].mean()
    if len(block_means) >= 2:
        slope, _ = np.polyfit(block_means.index, block_means.values, 1)
        vigilance_slope = float(slope)
    else:
        vigilance_slope = 0.0

    return {
        "participant_id": subj_id,
        "group": group_val,
        "is_compliant": is_compliant,
        "exclusion_reason": rejection_reason,
        "n_trials_raw": len(subj_df),
        "n_trials_retained_rt": len(retained_ax),
        "ax_hit_rate": round(ax_hit_rate, 5),
        "ay_commission_rate": round(ay_rate, 5),
        "bx_commission_rate": round(bx_rate, 5),
        "by_commission_rate": round(by_rate, 5),
        "omission_rate_global": round(omission_rate, 5),
        "anticipation_rate": round(anticipation_rate, 5),
        "rt_mean_ax_ms": round(rt_mean, 5),
        "rt_sd_ax_ms": round(rt_sd, 5),
        "rt_icv_ax": round(rt_icv, 5),
        "dprime_global": round(dp_glob, 5),
        "criterion_global": round(crit_glob, 5),
        "dprime_context": round(dp_ctx, 5),
        "pbi_index": round(pbi, 5),
        "conflict_cost_ms": round(conflict_cost, 5),
        "wm_decay_cost_pct": round(wm_decay_cost, 5),
        "pes_ms": round(pes, 5),
        "vigilance_slope_ms": round(vigilance_slope, 5),
        "mad_outlier_count": int(subj_df["flag_mad_outlier"].sum())
    }

# CPT_SUMMARIZE_AUDIT_INPUT_HARD_PATCH
import pandas as _cpt_sum_pd

try:
    from .clean import _cpt_hard_ensure_dataframe as _cpt_sum_ensure_dataframe
except Exception:
    def _cpt_sum_ensure_dataframe(df):
        return df


_cpt_sum_original_summarize = globals().get("summarize_subject_session")

if (
    _cpt_sum_original_summarize is not None
    and not getattr(_cpt_sum_original_summarize, "_cpt_sum_wrapped", False)
):

    def summarize_subject_session(*args, **kwargs):
        args = tuple(
            _cpt_sum_ensure_dataframe(arg)
            if isinstance(arg, _cpt_sum_pd.DataFrame)
            else arg
            for arg in args
        )

        kwargs = {
            key: _cpt_sum_ensure_dataframe(value)
            if isinstance(value, _cpt_sum_pd.DataFrame)
            else value
            for key, value in kwargs.items()
        }

        return _cpt_sum_original_summarize(*args, **kwargs)

    summarize_subject_session.__doc__ = getattr(_cpt_sum_original_summarize, "__doc__", None)
    summarize_subject_session.__wrapped__ = _cpt_sum_original_summarize
    summarize_subject_session._cpt_sum_wrapped = True

    globals()["summarize_subject_session"] = summarize_subject_session
