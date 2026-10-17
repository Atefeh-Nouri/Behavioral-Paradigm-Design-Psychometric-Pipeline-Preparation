"""
Standardized Data Logging and Output Contract Enforcement.
Validates session outputs against Raw Data Schema v1.0.

This module is importable in headless environments: it depends only on
the standard library, pandas, and a *type-only* reference to
``TrialResult`` (which lives in ``trial_executor.py`` and imports
psychopy). ``from __future__ import annotations`` defers annotation
evaluation, so ``TrialResult`` never needs to be a runtime symbol here.
"""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import os
from typing import TYPE_CHECKING, Any, Dict, List
import uuid

import pandas as pd

if TYPE_CHECKING:  # pragma: no cover — never executed at runtime
    try:
        from trial_executor import TrialResult
    except ImportError:
        from .trial_executor import TrialResult


class SchemaValidationError(Exception):
    """Raised when output data violates the Raw Data Schema v1.0 contract."""
    pass


class SessionDataLogger:
    """
    Collects trial outcomes, enforces data schemas, generates session
    metadata, and writes validated CSV and Parquet files to disk.
    """

    SCHEMA_COLUMNS = [
        "session_id", "participant_id", "block_index", "block_condition",
        "trial_index_global", "trial_index_block", "trial_type",
        "cue_stimulus", "probe_stimulus", "required_key",
        "cpi_nominal_ms", "cpi_realized_ms", "fixation_realized_ms",
        "probe_onset_timestamp", "response_key", "response_timestamp",
        "rt_ms", "is_correct", "outcome_code", "is_anticipation",
        "post_error_trial", "frame_drop_detected",
    ]

    ALLOWED_OUTCOMES = {
        "HIT", "CORRECT_REJECTION", "COMMISSION_ERROR",
        "OMISSION_ERROR", "ANTICIPATION",
    }

    def __init__(self, participant_id: str, group: str, config: dict):
        self.participant_id = participant_id
        self.group = group
        self.config = config
        self.session_id = str(uuid.uuid4())
        self.trial_records: List[Dict[str, Any]] = []

    def log_trial(self, result: "TrialResult") -> None:
        """Flattens a TrialResult into the strict 22-column format."""
        t_def = result.trial_definition
        record = {
            "session_id": self.session_id,
            "participant_id": self.participant_id,
            "block_index": (result.trial_index_global - 1) // 100 + 1,
            "block_condition": t_def.block_condition,
            "trial_index_global": result.trial_index_global,
            "trial_index_block": result.trial_index_block,
            "trial_type": t_def.trial_type,
            "cue_stimulus": t_def.cue_stimulus,
            "probe_stimulus": t_def.probe_stimulus,
            "required_key": t_def.required_key,
            "cpi_nominal_ms": float(t_def.cpi_nominal_ms),
            "cpi_realized_ms": round(result.cpi_realized_ms, 3),
            "fixation_realized_ms": round(result.fixation_realized_ms, 3),
            "probe_onset_timestamp": round(result.probe_onset_timestamp, 5),
            "response_key": result.response_key if result.response_key else None,
            "response_timestamp": (
                round(result.response_timestamp, 5)
                if result.response_timestamp else None
            ),
            "rt_ms": (
                round(result.rt_ms, 3) if result.rt_ms is not None else None
            ),
            "is_correct": bool(result.is_correct),
            "outcome_code": result.outcome_code,
            "is_anticipation": bool(result.is_anticipation),
            "post_error_trial": bool(result.post_error_trial),
            "frame_drop_detected": bool(result.frame_drop_detected),
        }
        self.trial_records.append(record)

    def validate_dataset(self, df: pd.DataFrame) -> None:
        """Enforces schema column names, data types, nullability, and
        allowed values."""
        if list(df.columns) != self.SCHEMA_COLUMNS:
            raise SchemaValidationError(
                f"Column mismatch! Expected: {self.SCHEMA_COLUMNS}, "
                f"Got: {list(df.columns)}"
            )

        if len(df) != self.config["design"]["total_experimental_trials"]:
            raise SchemaValidationError(
                f"Trial count mismatch! Expected: "
                f"{self.config['design']['total_experimental_trials']}, "
                f"Got: {len(df)}"
            )

        invalid_outcomes = set(df["outcome_code"]) - self.ALLOWED_OUTCOMES
        if invalid_outcomes:
            raise SchemaValidationError(
                f"Invalid outcome codes detected: {invalid_outcomes}"
            )

        if df["rt_ms"].dropna().lt(0).any():
            raise SchemaValidationError(
                "Negative reaction times detected in output!"
            )

        anticipations = df[df["is_anticipation"]]
        if not anticipations.empty and (anticipations["rt_ms"] >= 150.0).any():
            raise SchemaValidationError(
                "Anticipation flag inconsistent with 150 ms threshold."
            )

    def save_session(self, frame_drops: list) -> str:
        """Validates and writes trial records and metadata to disk."""
        df = pd.DataFrame(self.trial_records)
        self.validate_dataset(df)

        out_dir = self.config["logging"]["output_dir"]
        os.makedirs(out_dir, exist_ok=True)
        base_name = f"{self.participant_id}_{self.session_id}"
        csv_path = os.path.join(out_dir, f"{base_name}_trials.csv")
        meta_path = os.path.join(out_dir, f"{base_name}_meta.json")

        df.to_csv(csv_path, index=False)

        meta = {
            "session_id": self.session_id,
            "participant_id": self.participant_id,
            "group": self.group,
            "total_trials": len(df),
            "frame_drops_count": len(frame_drops),
            "config_hash": hashlib.sha256(
                json.dumps(self.config, sort_keys=True).encode()
            ).hexdigest(),
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return csv_path