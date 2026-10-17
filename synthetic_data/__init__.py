"""
Synthetic Behavioral Data Generation Package for AX-CPT.
Implements hierarchical Monte Carlo simulation based on Ex-Gaussian latency
convolutions, Signal Detection Theory threshold dynamics, and artifact injection.
"""

from .generator import SyntheticDataGenerator, SubjectTraits, inject_dataset_anomalies

__version__ = "1.0.0"
__all__ = [
    "SyntheticDataGenerator",
    "SubjectTraits",
    "inject_dataset_anomalies"
]
