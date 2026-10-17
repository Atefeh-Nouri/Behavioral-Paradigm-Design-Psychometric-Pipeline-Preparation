"""
Ingestion and Data Integrity Validation Layer.
Enforces Raw Data Schema v1.0, detects session anomalies,
and generates participant compliance logs.
"""

from dataclasses import dataclass
import glob
import os
from typing import List, Tuple

import numpy as np
import pandas as pd
import yaml


class SchemaIntegrityError(Exception):
    """Raised when incoming raw CSV files violate column structure or types."""
    pass


@dataclass
class SubjectValidationRecord:
    participant_id: str
    file_path: str
    raw_row_count: int
    has_schema_mismatch: bool
    duplicate_rows_detected: int
    missing_trials_detected: int
    ax_omission_rate: float
    anticipation_rate: float
    is_compliant: bool
    rejection_reason: str


class DataIngestor:
    """
    Ingests raw participant CSV files, applies strict schema assertions,
    detects technical logging anomalies, and flags non-compliant cohorts.
    """

    EXPECTED_COLUMNS = [
        "session_id", "participant_id", "block_index", "block_condition",
        "trial_index_global", "trial_index_block", "trial_type",
        "cue_stimulus", "probe_stimulus", "required_key",
        "cpi_nominal_ms", "cpi_realized_ms", "fixation_realized_ms",
        "probe_onset_timestamp", "response_key", "response_timestamp",
        "rt_ms", "is_correct", "outcome_code", "is_anticipation",
        "post_error_trial", "frame_drop_detected",
    ]

    EXPECTED_DTYPES = {
        "session_id": "object",
        "participant_id": "object",
        "block_index": "int64",
        "block_condition": "object",
        "trial_index_global": "int64",
        "trial_index_block": "int64",
        "trial_type": "object",
        "cue_stimulus": "object",
        "probe_stimulus": "object",
        "required_key": "object",
        "cpi_nominal_ms": "float64",
        "cpi_realized_ms": "float64",
        "fixation_realized_ms": "float64",
        "probe_onset_timestamp": "float64",
        "response_key": "object",
        "response_timestamp": "float64",
        "rt_ms": "float64",
        "is_correct": "bool",
        "outcome_code": "object",
        "is_anticipation": "bool",
        "post_error_trial": "bool",
        "frame_drop_detected": "bool",
    }

    # Frozen-spec defaults (PSD v1.0 / Day-19 pipeline_config contract).
    _DEFAULT_DEDUP_SUBSET = ["participant_id", "trial_index_global"]
    _DEFAULT_DEDUP_KEEP = "first"
    _DEFAULT_MIN_TRIALS = 380
    _DEFAULT_MAX_AX_OMISSION_RATE = 0.15
    _DEFAULT_MAX_ANTICIPATION_RATE = 0.10
    _DEFAULT_EXPECTED_TRIAL_COUNT = 400
    _DEFAULT_RAW_DATA_DIR = "data/raw"

    def __init__(self, config_path: str = "config/pipeline_config.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Pipeline configuration not found at: {config_path}"
            )
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}

        # Fail fast with actionable diagnosis if the wrong config file was passed.
        if not isinstance(self.config, dict) or "cleaning_rules" not in self.config:
            raise ValueError(
                f"{config_path} does not appear to be a pipeline_config.yaml "
                f"(missing top-level 'cleaning_rules'). "
                f"Top-level keys found: {list(self.config.keys()) if isinstance(self.config, dict) else type(self.config).__name__}"
            )

    # ------------------------------------------------------------------
    # Structure validation
    # ------------------------------------------------------------------
    def validate_file_structure(self, df: pd.DataFrame, file_path: str) -> None:
        """Asserts exact column order, names, and allowable categorical values."""
        if list(df.columns) != self.EXPECTED_COLUMNS:
            raise SchemaIntegrityError(
                f"File {file_path} failed column contract!\n"
                f"Expected: {self.EXPECTED_COLUMNS}\n"
                f"Got:      {list(df.columns)}"
            )

        for col, expected_dtype in self.EXPECTED_DTYPES.items():
            actual_dtype = str(df[col].dtype)
            if actual_dtype != expected_dtype:
                # pandas reads int columns containing nulls as float64
                if not (
                    expected_dtype == "int64"
                    and actual_dtype in ("int64", "float64")
                ):
                    raise SchemaIntegrityError(
                        f"File {file_path} column '{col}' type mismatch! "
                        f"Expected {expected_dtype}, got {actual_dtype}"
                    )

    # ------------------------------------------------------------------
    # Config accessors with safe defaults
    # ------------------------------------------------------------------
    def _get_dedup_config(self) -> Tuple[List[str], str]:
        clean_rules = self.config.get("cleaning_rules", {}) or {}
        dedup_cfg = clean_rules.get("deduplication", {}) or {}
        subset = dedup_cfg.get("subset", self._DEFAULT_DEDUP_SUBSET)
        keep = dedup_cfg.get("keep", self._DEFAULT_DEDUP_KEEP)
        if not isinstance(subset, (list, tuple)) or not subset:
            subset = self._DEFAULT_DEDUP_SUBSET
        if keep not in ("first", "last", False):
            keep = self._DEFAULT_DEDUP_KEEP
        return list(subset), keep

    def _get_compliance_thresholds(self) -> dict:
        thresh = self.config.get("compliance_thresholds", {}) or {}
        return {
            "min_trials_required": float(
                thresh.get("min_trials_required", self._DEFAULT_MIN_TRIALS)
            ),
            "max_ax_omission_rate": float(
                thresh.get("max_ax_omission_rate", self._DEFAULT_MAX_AX_OMISSION_RATE)
            ),
            "max_anticipation_rate": float(
                thresh.get("max_anticipation_rate", self._DEFAULT_MAX_ANTICIPATION_RATE)
            ),
        }

    def _get_expected_trial_count(self) -> int:
        # Prefer experimental config total if available; else PSD default.
        design = self.config.get("design", {}) or {}
        try:
            return int(design.get("total_experimental_trials", self._DEFAULT_EXPECTED_TRIAL_COUNT))
        except (TypeError, ValueError):
            return self._DEFAULT_EXPECTED_TRIAL_COUNT

    def _get_raw_data_dir(self) -> str:
        io_cfg = self.config.get("io", {}) or {}
        return io_cfg.get("raw_data_dir", self._DEFAULT_RAW_DATA_DIR)

    # ------------------------------------------------------------------
    # Subject session audit
    # ------------------------------------------------------------------
    def audit_subject_session(
        self,
        df: pd.DataFrame,
        file_path: str,
    ) -> Tuple[pd.DataFrame, SubjectValidationRecord]:
        """Audits trial continuity, duplicates, and psychometric compliance."""
        self.validate_file_structure(df, file_path)

        participant_id = str(df["participant_id"].iloc[0])
        total_rows = len(df)

        # 1. Audit duplicates (safe config access; no KeyError possible)
        dedup_subset, dedup_keep = self._get_dedup_config()
        dup_mask = df.duplicated(subset=dedup_subset, keep=dedup_keep)
        duplicate_count = int(dup_mask.sum())

        df = df.copy()
        df["flag_duplicate_row"] = dup_mask.astype(bool)

        # 2. Audit trial continuity
        unique_indices = df.loc[~dup_mask, "trial_index_global"].values
        expected_count = self._get_expected_trial_count()
        expected_indices = np.arange(1, expected_count + 1)
        missing_count = int(
            len(set(expected_indices.tolist()) - set(np.asarray(unique_indices).tolist()))
        )
        df["flag_dropped_trial"] = False

        # 3. Psychometric compliance evaluation (safe config access)
        thresh = self._get_compliance_thresholds()

        ax_mask = (df["trial_type"] == "AX") & (~df["flag_duplicate_row"])
        ax_trials = df.loc[ax_mask]
        ax_total = len(ax_trials)
        if ax_total > 0:
            ax_omissions = int((ax_trials["outcome_code"] == "OMISSION_ERROR").sum())
            ax_omission_rate = ax_omissions / ax_total
        else:
            ax_omission_rate = 1.0

        if total_rows > 0:
            anticipations = int((df["outcome_code"] == "ANTICIPATION").sum())
            anticipation_rate = anticipations / total_rows
        else:
            anticipation_rate = 1.0

        is_compliant = True
        rejection_reason = "NONE"

        if total_rows < thresh["min_trials_required"]:
            is_compliant = False
            rejection_reason = f"INSUFFICIENT_TRIALS_COUNT_{total_rows}"
        elif ax_omission_rate > thresh["max_ax_omission_rate"]:
            is_compliant = False
            rejection_reason = f"EXCESSIVE_AX_OMISSIONS_{ax_omission_rate:.4f}"
        elif anticipation_rate > thresh["max_anticipation_rate"]:
            is_compliant = False
            rejection_reason = f"EXCESSIVE_ANTICIPATIONS_{anticipation_rate:.4f}"

        record = SubjectValidationRecord(
            participant_id=participant_id,
            file_path=file_path,
            raw_row_count=total_rows,
            has_schema_mismatch=False,
            duplicate_rows_detected=duplicate_count,
            missing_trials_detected=missing_count,
            ax_omission_rate=round(float(ax_omission_rate), 4),
            anticipation_rate=round(float(anticipation_rate), 4),
            is_compliant=is_compliant,
            rejection_reason=rejection_reason,
        )

        return df, record

    # ------------------------------------------------------------------
    # Batch ingestion
    # ------------------------------------------------------------------
    def ingest_all_sessions(self) -> Tuple[pd.DataFrame, List[SubjectValidationRecord]]:
        """Ingests and validates all matching participant files in the raw data directory."""
        raw_dir = self._get_raw_data_dir()
        search_pattern = os.path.join(raw_dir, "SUBJ_*_raw_trials.csv")
        file_list = sorted(glob.glob(search_pattern))

        if not file_list:
            raise FileNotFoundError(
                f"No participant raw files found matching {search_pattern}"
            )

        all_dfs = []
        validation_records = []

        for f_path in file_list:
            raw_df = pd.read_csv(f_path)
            audited_df, val_record = self.audit_subject_session(raw_df, f_path)
            all_dfs.append(audited_df)
            validation_records.append(val_record)

        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df, validation_records