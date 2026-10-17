"""
AX-CPT PsychoPy Coder Implementation Package.

Provides frame-accurate stimulus timing, low-latency keyboard polling,
rejection-sampled trial sequencing, and Raw Data Schema v1.0 logging.

Submodules are loaded lazily (PEP 562) so that pure-Python helpers —
``config_loader``, ``trial_logic``, ``logger`` — can be imported in
headless CI environments where ``psychopy`` is not installed. Attributes
that genuinely require ``psychopy`` (``engine``, ``trial_executor``,
``ui``) raise ``ImportError`` only on first access, with the same message
a direct submodule import would produce. Public API is unchanged.
"""

from importlib import import_module
from typing import Any

__version__ = "1.0.0"

# name -> (submodule, attribute_in_submodule)
_LAZY_ATTRS = {
    "load_experiment_config": (".config_loader", "load_experiment_config"),
    "PsychopyEngine":         (".engine",         "PsychopyEngine"),
    "EngineClockManager":     (".engine",         "EngineClockManager"),
    "FrameDropEvent":         (".engine",         "FrameDropEvent"),
    "TrialSequenceGenerator": (".trial_logic",    "TrialSequenceGenerator"),
    "TrialDefinition":        (".trial_logic",    "TrialDefinition"),
    "TrialExecutor":          (".trial_executor", "TrialExecutor"),
    "TrialResult":            (".trial_executor", "TrialResult"),
    "UIManager":              (".ui",             "UIManager"),
    "PracticeManager":        (".ui",             "PracticeManager"),
    "SessionDataLogger":      (".logger",         "SessionDataLogger"),
    "SchemaValidationError":  (".logger",         "SchemaValidationError"),
}

__all__ = sorted(_LAZY_ATTRS) + ["__version__"]


def __getattr__(name: str) -> Any:
    """Resolve ``paradigms.psychopy.<name>`` lazily on first access."""
    if name in _LAZY_ATTRS:
        submodule, attr = _LAZY_ATTRS[name]
        module = import_module(submodule, __name__)
        return getattr(module, attr)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)