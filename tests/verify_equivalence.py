"""
Cross-Language Equivalence Verifier: Python ↔ R Pipeline Parity Audit.

Compares cleaned_trials.parquet (Python) against cleaned_trials_r.csv (R).
Python produces 36 columns; R produces 31. The 5 Python-only audit columns
are verified for dtype/nullability but excluded from the shared numeric
comparison. All 31 R columns are shared and are compared row-by-row.

Exit codes:
  0  All parity checks passed
  1  Parity violation(s) detected
  2  I/O or configuration error
"""

import argparse
import sys
import os

import numpy as np
import pandas as pd
import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Python produces 36 columns; R produces 31. These 5 flags are Python-only
# and are verified for nullability/dtype but NOT compared against R.
#
# Contract — keep this list in sync with the Python pipeline:
#   analysis_python/cpt_pipeline.py  (source of truth)
# The definitive test is:
#   py_only = set(py_df.columns) - set(r_cols_in_R_script)
# Any name listed here MUST exist in Python's output and MUST NOT exist in
# R's `python_col_order`. Otherwise the verifier either drops a shared
# column from comparison (silent coverage loss) or emits a dead INFO line.
PYTHON_ONLY_AUDIT_COLUMNS: list[str] = [
    "flag_missing_trial",
    "flag_frame_drop",
    "flag_response_window_violation",
    "flag_schema_invalid",
    "flag_excluded",
]

# Row sort key — must be present in both outputs.
SORT_KEY: list[str] = ["participant_id", "trial_index_global"]

# Default numerical tolerance (matches cpt_cleaning_pipeline.R target: 1e-5).
DEFAULT_ATOL: float = 1e-5
DEFAULT_RTOL: float = 1e-5

# Default I/O paths — overridable via CLI or pipeline_config.yaml.
#
# IMPORTANT: these paths MUST match the artifact layout produced by
# .github/workflows/pipeline_ci.yml:
#   - Python job uploads   data/processed/python/   → cleaned_trials.parquet
#   - R job uploads        data/processed/r/        → cleaned_trials_r.csv
DEFAULT_PY_OUTPUT: str = "data/processed/python/cleaned_trials.parquet"
DEFAULT_R_OUTPUT:  str = "data/processed/r/cleaned_trials_r.csv"
DEFAULT_CONFIG:    str = "config/pipeline_config.yaml"


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def _load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        # Non-fatal: caller may rely on built-in defaults (useful for local runs).
        print(
            f"WARNING: config file not found at '{config_path}', "
            f"falling back to built-in tolerances.",
            file=sys.stderr,
        )
        return {}
    with open(config_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


# ---------------------------------------------------------------------------
# NA normalisation
# ---------------------------------------------------------------------------

def _normalise_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unify NA representations across Python (NaN) and R (string 'NA', 'N/A').
    Operates in-place on object columns.
    """
    na_sentinels = {"NA", "N/A", "nan", "NaN", ""}
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].where(~df[col].isin(na_sentinels), other=np.nan)
    return df


# ---------------------------------------------------------------------------
# Column alignment
# ---------------------------------------------------------------------------

def _align(
    py_df: pd.DataFrame,
    r_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str], list[str]]:
    """
    1. Drop known Python-only audit columns from py_df.
    2. Determine shared columns; warn on asymmetric extras.
    3. Sort both frames by SORT_KEY.
    4. Return (py_aligned, r_aligned, shared_cols, warnings).

    Raises
    ------
    ValueError
        If any SORT_KEY column is missing from the shared schema — without
        a stable sort key, row-wise parity comparison is meaningless.
    """
    warnings: list[str] = []

    audit_present = [c for c in PYTHON_ONLY_AUDIT_COLUMNS if c in py_df.columns]
    py_core = py_df.drop(columns=audit_present)

    only_py = set(py_core.columns) - set(r_df.columns)
    only_r  = set(r_df.columns) - set(py_core.columns)

    if only_py:
        warnings.append(
            f"  WARNING: {len(only_py)} column(s) only in Python output "
            f"(not in R): {sorted(only_py)}"
        )
    if only_r:
        warnings.append(
            f"  WARNING: {len(only_r)} column(s) only in R output "
            f"(not in Python): {sorted(only_r)}"
        )

    shared = [c for c in py_core.columns if c in r_df.columns]

    missing_sort_keys = [k for k in SORT_KEY if k not in shared]
    if missing_sort_keys:
        raise ValueError(
            f"Sort key column(s) missing from shared schema: {missing_sort_keys}. "
            f"Shared columns are: {shared}. "
            f"Cannot verify row-wise parity without a stable sort key."
        )

    def _sort(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df[shared]
            .sort_values(SORT_KEY)
            .reset_index(drop=True)
        )

    return _sort(py_core), _sort(r_df), shared, warnings


# ---------------------------------------------------------------------------
# Core comparison
# ---------------------------------------------------------------------------

def _compare(
    py: pd.DataFrame,
    r: pd.DataFrame,
    shared: list[str],
    atol: float,
    rtol: float,
) -> list[str]:
    """
    Column-by-column parity check with three comparison strategies:
      - bool columns  → exact match (NA → False)
      - numeric cols  → np.isclose(atol, rtol), NaN-position checked separately
      - string/cat    → exact match after NA unification
    Returns a list of failure messages (empty list = full parity).
    """
    failures: list[str] = []

    if len(py) != len(r):
        failures.append(
            f"  FAIL: Row count mismatch — Python {len(py):,} rows vs R {len(r):,} rows "
            f"(delta: {len(py) - len(r):+,})."
        )
        return failures  # column comparison undefined at different lengths

    for col in shared:
        py_col = py[col]
        r_col  = r[col]

        # ---- boolean --------------------------------------------------------
        if pd.api.types.is_bool_dtype(py_col) or pd.api.types.is_bool_dtype(r_col):
            py_b = py_col.fillna(False).astype(bool)
            r_b  = r_col.fillna(False).astype(bool)
            n_diff = int((py_b != r_b).sum())
            if n_diff:
                failures.append(f"  FAIL [{col}]: boolean mismatch in {n_diff} row(s).")
            continue

        # ---- numeric --------------------------------------------------------
        if pd.api.types.is_numeric_dtype(py_col) or pd.api.types.is_numeric_dtype(r_col):
            py_num = pd.to_numeric(py_col, errors="coerce")
            r_num  = pd.to_numeric(r_col,  errors="coerce")

            py_na, r_na = py_num.isna(), r_num.isna()
            na_mismatch = int((py_na != r_na).sum())
            if na_mismatch:
                failures.append(
                    f"  FAIL [{col}]: NA/NaN position mismatch in {na_mismatch} row(s)."
                )

            valid = ~py_na & ~r_na
            if valid.any():
                close = np.isclose(
                    py_num[valid].to_numpy(),
                    r_num[valid].to_numpy(),
                    atol=atol,
                    rtol=rtol,
                    equal_nan=False,
                )
                if not close.all():
                    n_diff = int((~close).sum())
                    max_delta = float(
                        np.max(np.abs(py_num[valid].to_numpy() - r_num[valid].to_numpy()))
                    )
                    failures.append(
                        f"  FAIL [{col}]: numeric mismatch in {n_diff} row(s); "
                        f"max |Δ| = {max_delta:.3e}  (atol={atol}, rtol={rtol})."
                    )
            continue

        # ---- string / categorical -------------------------------------------
        py_s = py_col.fillna("__NA__").astype(str)
        r_s  = r_col.fillna("__NA__").astype(str)
        n_diff = int((py_s != r_s).sum())
        if n_diff:
            failures.append(f"  FAIL [{col}]: string mismatch in {n_diff} row(s).")

    return failures


# ---------------------------------------------------------------------------
# Audit-flag consistency (Python-only columns)
# ---------------------------------------------------------------------------

def _check_audit_flags(py_df: pd.DataFrame) -> list[str]:
    """
    Validates Python-only audit flags for dtype and completeness.
    These columns do not exist in R output; no cross-language comparison is done.
    """
    issues: list[str] = []
    for col in PYTHON_ONLY_AUDIT_COLUMNS:
        if col not in py_df.columns:
            issues.append(f"  INFO  [{col}]: column absent from Python output.")
            continue
        n_null = int(py_df[col].isna().sum())
        if n_null:
            issues.append(
                f"  WARN  [{col}]: {n_null} null value(s) in audit flag column "
                f"(expected all-boolean)."
            )
    return issues


# ---------------------------------------------------------------------------
# Tolerance resolution
# ---------------------------------------------------------------------------

def _resolve_tolerances(
    cfg: dict,
    cli_atol: float | None,
    cli_rtol: float | None,
) -> tuple[float, float]:
    """
    Resolve (atol, rtol) in most-specific → least-specific order:

      1. CLI --atol / --rtol                         (explicit override)
      2. config.equivalence_check.atol / .rtol       (preferred key)
      3. config.numerical_precision.float_tolerance_equivalence  (legacy)
      4. DEFAULT_ATOL / DEFAULT_RTOL                 (built-in, 1e-5)

    The legacy fallback guarantees that the R pipeline's own tolerance
    contract is *not* silently loosened to the built-in default when the
    explicit `equivalence_check` block is absent.
    """
    eq_cfg     = cfg.get("equivalence_check", {}) or {}
    legacy_tol = (cfg.get("numerical_precision", {}) or {}).get(
        "float_tolerance_equivalence"
    )

    cfg_atol = eq_cfg.get(
        "atol", legacy_tol if legacy_tol is not None else DEFAULT_ATOL
    )
    cfg_rtol = eq_cfg.get(
        "rtol", legacy_tol if legacy_tol is not None else DEFAULT_RTOL
    )

    atol = float(cli_atol) if cli_atol is not None else float(cfg_atol)
    rtol = float(cli_rtol) if cli_rtol is not None else float(cfg_rtol)
    return atol, rtol


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="CPT Pipeline — Python ↔ R cleaned-trial equivalence verifier."
    )
    parser.add_argument("--py-output", default=DEFAULT_PY_OUTPUT,
                        help="Path to cleaned_trials.parquet (Python output).")
    parser.add_argument("--r-output",  default=DEFAULT_R_OUTPUT,
                        help="Path to cleaned_trials_r.csv (R output).")
    parser.add_argument("--config",    default=DEFAULT_CONFIG,
                        help="Path to pipeline_config.yaml.")
    parser.add_argument("--atol",      type=float, default=None,
                        help="Absolute tolerance override.")
    parser.add_argument("--rtol",      type=float, default=None,
                        help="Relative tolerance override.")
    args = parser.parse_args(argv)

    cfg = _load_config(args.config)
    atol, rtol = _resolve_tolerances(cfg, args.atol, args.rtol)

    SEP = "=" * 70
    print(SEP)
    print("CPT Pipeline — Python ↔ R Equivalence Report")
    print(f"  Python : {args.py_output}")
    print(f"  R      : {args.r_output}")
    print(f"  tol    : atol={atol}, rtol={rtol}")
    print(SEP)

    # ---- load ---------------------------------------------------------------
    try:
        py_df = pd.read_parquet(args.py_output)
    except Exception as exc:
        print(f"ERROR: cannot load Python output — {exc}", file=sys.stderr)
        return 2

    try:
        r_df = pd.read_csv(args.r_output)
    except Exception as exc:
        print(f"ERROR: cannot load R output — {exc}", file=sys.stderr)
        return 2

    # ---- normalise ----------------------------------------------------------
    py_df = _normalise_na(py_df)
    r_df  = _normalise_na(r_df)

    # ---- audit flags (Python-only) ------------------------------------------
    audit_issues = _check_audit_flags(py_df)
    if audit_issues:
        print("\n[Audit flags — Python-only, not compared against R]")
        for msg in audit_issues:
            print(msg)

    # ---- column alignment ---------------------------------------------------
    try:
        py_aln, r_aln, shared, align_warnings = _align(py_df, r_df)
    except ValueError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 2

    audit_found = [c for c in PYTHON_ONLY_AUDIT_COLUMNS if c in py_df.columns]
    print(f"\n[Column alignment]")
    print(f"  Python total cols      : {len(py_df.columns)}")
    print(f"  Python-only audit cols : {len(audit_found)}  {audit_found}")
    print(f"  R cols                 : {len(r_df.columns)}")
    print(f"  Shared (tested)        : {len(shared)}")
    for w in align_warnings:
        print(w)

    # ---- row counts ---------------------------------------------------------
    print(f"\n[Row counts after sort]")
    print(f"  Python : {len(py_aln):,}")
    print(f"  R      : {len(r_aln):,}")
    if len(py_aln) != len(r_aln):
        print(f"  DELTA  : {len(py_aln) - len(r_aln):+,}  ← investigate deduplication logic")

    # ---- compare ------------------------------------------------------------
    failures = _compare(py_aln, r_aln, shared, atol=atol, rtol=rtol)

    # ---- report -------------------------------------------------------------
    print(f"\n[Parity results — {len(shared)} shared columns]")
    if not failures:
        print(f"  PASS: all {len(shared)} columns within tolerance.")
        print(f"\nResult: EQUIVALENT")
        print(SEP)
        return 0

    for msg in failures:
        print(msg)
    print(f"\nResult: {len(failures)} FAILURE(S)")
    print(SEP)
    return 1


if __name__ == "__main__":
    sys.exit(main())