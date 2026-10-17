"""AX-CPT PsychoPy Coder Implementation Package.

Provides frame-accurate stimulus timing, low-latency keyboard polling,
rejection-sampled trial sequencing, and Raw Data Schema v1.0 logging.

Note: Heavy hardware/GUI imports (PsychopyEngine, etc.) are wrapped in try/except
to allow lightweight unit testing (e.g., Logger, TrialLogic) in environments
where PsychoPy/PsychToolbox is not installed (like GitHub Actions CI).
"""

# Always import pure-Python logic components first
from .config_loader import load_experiment_config
from .trial_logic import TrialSequenceGenerator, TrialDefinition
from .logger import SessionDataLogger, SchemaValidationError

__version__ = "1.0.0"

# Conditional imports for Hardware/GUI components
# These require 'psychopy' which may not be present in CI test environments
try:
    from .engine import PsychopyEngine, EngineClockManager, FrameDropEvent
    from .trial_executor import TrialExecutor, TrialResult
    from .ui import UIManager, PracticeManager
    
    # Update __all__ if hardware modules are available
    __all__ = [
        "load_experiment_config",
        "TrialSequenceGenerator",
        "TrialDefinition",
        "SessionDataLogger",
        "SchemaValidationError",
        "PsychopyEngine",
        "EngineClockManager",
        "FrameDropEvent",
        "TrialExecutor",
        "TrialResult",
        "UIManager",
        "PracticeManager",
    ]
except ImportError:
    # If psychopy is missing, we still expose the pure-logic components
    # This allows tests like test_logger_schema.py to pass
    __all__ = [
        "load_experiment_config",
        "TrialSequenceGenerator",
        "TrialDefinition",
        "SessionDataLogger",
        "SchemaValidationError",
    ]
