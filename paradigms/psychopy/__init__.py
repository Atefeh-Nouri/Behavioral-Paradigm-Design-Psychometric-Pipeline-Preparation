"""
AX-CPT PsychoPy Coder Implementation Package.
Provides frame-accurate stimulus timing, low-latency keyboard polling,
rejection-sampled trial sequencing, and Raw Data Schema v1.0 logging.
"""

from .config_loader import load_experiment_config
from .engine import PsychopyEngine, EngineClockManager, FrameDropEvent
from .trial_logic import TrialSequenceGenerator, TrialDefinition
from .trial_executor import TrialExecutor, TrialResult
from .ui import UIManager, PracticeManager
from .logger import SessionDataLogger, SchemaValidationError

__version__ = "1.0.0"
__all__ = [
    "load_experiment_config",
    "PsychopyEngine",
    "EngineClockManager",
    "FrameDropEvent",
    "TrialSequenceGenerator",
    "TrialDefinition",
    "TrialExecutor",
    "TrialResult",
    "UIManager",
    "PracticeManager",
    "SessionDataLogger",
    "SchemaValidationError",
]
