"""
Ingestion and Data Integrity Validation Layer.
Enforces Raw Data Schema v1.0, detects session anomalies,
and generates participant compliance logs.
"""

from dataclasses import dataclass, asdict
import glob
import json
import os
from typing import Any, Dict, List, Tuple
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
        "post_error_trial", "frame_drop_detected"
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
        "frame_drop_detected": "bool"
    }

    def __init__(self, config_path: str = "config/pipeline_config.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Pipeline configuration not found at: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def validate_file_structure(self, df: pd.DataFrame, file_path: str) -> None:
        """Asserts exact column order, names, and allowable categorical values."""
        if list(df.columns) != self.EXPECTED_COLUMNS:
            raise SchemaIntegrityError(
                f"File {file_path} failed column contract!\n"
                f"Expected: {self.EXPECTED_COLUMNS}\nGot: {list(df.columns)}"
            )

        for col, expected_dtype in self.EXPECTED_DTYPES.items():
            actual_dtype = str(df[col].dtype)
            if actual_dtype != expected_dtype:
                # Handle pandas reading integer columns with nulls as float64
                if not (expected_dtype == "int64" and actual_dtype in ["int64", "float64"]):
                    raise SchemaIntegrityError(
                        f"File {file_path} column '{col}' type mismatch! "
                        f"Expected {expected_dtype}, got {actual_dtype}"
                    )

    def audit_subject_session(self, df: pd.DataFrame, file_path: str) -> Tuple[pd.DataFrame, SubjectValidationRecord]:
        """Audits trial continuity, duplicates, and psychometric compliance."""
        self.validate_file_structure(df, file_path)
        participant_id = str(df["participant_id"].iloc[0])
        total_rows = len(df)

        # 1. Audit Duplicates
        dedup_cfg = self.config["cleaning_rules"]["deduplication"]
        dup_mask = df.duplicated(subset=dedup_cfg["subset"], keep=dedup_cfg["keep"])
        duplicate_count = int(dup_mask.sum())

        # Non-destructively tag duplicates
        df = df.copy()
        df["flag_duplicate_row"] = dup_mask

        # 2. Audit Trial Continuity (Missing rows)
        unique_indices = df.loc[~dup_mask, "trial_index_global"].values
        expected_indices = np.arange(1, 401)
        missing_count = int(len(set(expected_indices) - set(unique_indices)))
        df["flag_dropped_trial"] = False

        # 3. Psychometric Compliance Evaluation
        thresh = self.config["compliance_thresholds"]
        ax_trials = df[(df["trial_type"] == "AX") & (~df["flag_duplicate_row"])]
        ax_omissions = (ax_trials["outcome_code"] == "OMISSION_ERROR").sum()
        ax_omission_rate = float(ax_omissions / len(ax_trials)) if len(ax_trials) > 0 else 1.0

        anticipations = (df["outcome_code"] == "ANTICIPATION").sum()
        anticipation_rate = float(anticipations / total_rows) if total_rows > 0 else 1.0

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
            ax_omission_rate=round(ax_omission_rate, 4),
            anticipation_rate=round(anticipation_rate, 4),
            is_compliant=is_compliant,
            rejection_reason=rejection_reason
        )

        return df, record

    def ingest_all_sessions(self) -> Tuple[pd.DataFrame, List[SubjectValidationRecord]]:
        """Ingests and validates all matching participant files in the raw data directory."""
        raw_dir = self.config["io"]["raw_data_dir"]
        search_pattern = os.path.join(raw_dir, "SUBJ_*_raw_trials.csv")
        file_list = sorted(glob.glob(search_pattern))

        if not file_list:
            raise FileNotFoundError(f"No participant raw files found matching {search_pattern}")

        all_dfs = []
        validation_records = []

        for f_path in file_list:
            raw_df = pd.read_csv(f_path)
            audited_df, val_record = self.audit_subject_session(raw_df, f_path)
            all_dfs.append(audited_df)
            validation_records.append(val_record)

        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df, validation_records
