"""
AX-CPT Psychometric Data Processing Package (Python Implementation, Deliverable D6).
Provides schema-validated ingestion, non-destructive MAD latency cleaning,
Hautus log-linear Signal Detection Theory scoring, and subject aggregation.
"""

from .ingest import DataIngestor, SchemaIntegrityError, SubjectValidationRecord
from .clean import compute_within_subject_mad_bounds, flag_trial_anomalies
from .sdt import calculate_hautus_sdt
from .summarize import summarize_subject_session
from .cpt_pipeline import run_pipeline

__version__ = "1.0.0"
__all__ = [
    "DataIngestor",
    "SchemaIntegrityError",
    "SubjectValidationRecord",
    "compute_within_subject_mad_bounds",
    "flag_trial_anomalies",
    "calculate_hautus_sdt",
    "summarize_subject_session",
    "run_pipeline",
]
