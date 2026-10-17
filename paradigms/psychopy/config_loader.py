"""
Configuration Loader and Validation Engine.
Loads config.yaml and enforces structural integrity and value bounds via Pydantic.
Supports dual-key alias resolution for robust pipeline execution.
"""

import os
from typing import List, Dict, Any, Optional
import yaml
from pydantic import BaseModel, Field, model_validator


class EnvironmentConfig(BaseModel):
    screen_number: int = Field(default=0, ge=0)
    fullscreen: bool = True
    window_resolution: List[int] = Field(default=[1920, 1080], min_length=2, max_length=2)
    background_color: List[float] = Field(default=[-1.0, -1.0, -1.0], min_length=3, max_length=3)
    units: str = "height"
    target_refresh_hz: float = Field(default=60.0, gt=0.0)
    refresh_tolerance_hz: float = Field(default=1.0, ge=0.0)
    allow_gui: bool = False
    cursor_visible: bool = False


class HardwareConfig(BaseModel):
    keyboard_backend: str = "ptb"
    target_key: str = "space"
    non_target_key: str = "l"
    abort_key: str = "escape"


class FixationTiming(BaseModel):
    nominal_ms: float = 500.0
    jitter_min_ms: float = 400.0
    jitter_max_ms: float = 600.0


class StimulusTiming(BaseModel):
    duration_ms: float = 300.0
    frames_at_60hz: int = 18
    frames_at_144hz: int = 43


class DelayTiming(BaseModel):
    short_delay_ms: float = 1200.0
    short_frames_at_60hz: int = 72
    long_delay_ms: float = 4000.0
    long_frames_at_60hz: int = 240


class ITITiming(BaseModel):
    nominal_ms: float = 1200.0
    jitter_min_ms: float = 1000.0
    jitter_max_ms: float = 1400.0


class TimingConfig(BaseModel):
    fixation: FixationTiming = Field(default_factory=FixationTiming)
    stimulus: StimulusTiming = Field(default_factory=StimulusTiming)
    delays: DelayTiming = Field(default_factory=DelayTiming)
    response_window_ms: float = 1000.0
    iti: ITITiming = Field(default_factory=ITITiming)
    anticipation_threshold_ms: float = 150.0
    break_duration_seconds: float = 60.0
    max_break_duration_seconds: float = 180.0


class StimuliConfig(BaseModel):
    text_height: float = 0.12
    font: str = "Arial"
    font_color: List[float] = Field(default=[1.0, 1.0, 1.0], min_length=3, max_length=3)
    cue_valid: str = "A"
    cue_invalid_set: List[str] = Field(default=["B", "C", "D", "E", "F", "G"])
    probe_valid: str = "X"
    probe_invalid_set: List[str] = Field(default=["S", "T", "U", "V", "W", "Z"])


class BlockDistributionConfig(BaseModel):
    ax: int = 70
    ay: int = 10
    bx: int = 10
    by: int = 10
    ax_count: int = 70
    ay_count: int = 10
    bx_count: int = 10
    by_count: int = 10

    @model_validator(mode="before")
    @classmethod
    def sync_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Sync between ax and ax_count
            if "ax" in data and "ax_count" not in data:
                data["ax_count"] = data["ax"]
            elif "ax_count" in data and "ax" not in data:
                data["ax"] = data["ax_count"]

            if "ay" in data and "ay_count" not in data:
                data["ay_count"] = data["ay"]
            elif "ay_count" in data and "ay" not in data:
                data["ay"] = data["ay_count"]

            if "bx" in data and "bx_count" not in data:
                data["bx_count"] = data["bx"]
            elif "bx_count" in data and "bx" not in data:
                data["bx"] = data["bx_count"]

            if "by" in data and "by_count" not in data:
                data["by_count"] = data["by"]
            elif "by_count" in data and "by" not in data:
                data["by"] = data["by_count"]
        return data


class RunRulesConfig(BaseModel):
    max_consecutive_targets: int = 4
    max_consecutive_nontargets: int = 2
    no_consecutive_identical_distractors: bool = True


class CounterbalancingConfig(BaseModel):
    group_a: List[str] = Field(default=["SHORT_DELAY", "LONG_DELAY", "LONG_DELAY", "SHORT_DELAY"])
    group_b: List[str] = Field(default=["LONG_DELAY", "SHORT_DELAY", "SHORT_DELAY", "LONG_DELAY"])


class DesignConfig(BaseModel):
    total_blocks: int = 4
    trials_per_block: int = 100
    total_experimental_trials: int = 400
    counterbalancing_groups: CounterbalancingConfig = Field(default_factory=CounterbalancingConfig)
    block_distribution: BlockDistributionConfig = Field(default_factory=BlockDistributionConfig)
    run_rules: RunRulesConfig = Field(default_factory=RunRulesConfig)


class PracticeDistribution(BaseModel):
    ax_count: int = 14
    ay_count: int = 2
    bx_count: int = 2
    by_count: int = 2


class PracticeConfig(BaseModel):
    total_trials: int = 20
    distribution: PracticeDistribution = Field(default_factory=PracticeDistribution)
    feedback_duration_ms: float = 800.0
    passing_accuracy_ratio: float = 0.80
    max_allowed_target_omissions: int = 0
    max_practice_attempts: int = 3


class CalibrationConfig(BaseModel):
    srt_trials: int = 30
    practice: PracticeConfig = Field(default_factory=PracticeConfig)


class LoggingConfig(BaseModel):
    output_dir: str = "data/raw"
    schema_version: str = "1.0"
    save_frame_intervals: bool = True


class ExperimentConfig(BaseModel):
    version: str = "1.0.0"
    experiment_name: str = "dual_delay_ax_cpt"
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)
    hardware: HardwareConfig = Field(default_factory=HardwareConfig)
    timing: TimingConfig = Field(default_factory=TimingConfig)
    stimuli: StimuliConfig = Field(default_factory=StimuliConfig)
    design: DesignConfig = Field(default_factory=DesignConfig)
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_experiment_config(config_path: str = "config/config.yaml") -> dict:
    """
    Loads and validates the experiment configuration YAML file.
    Returns the validated configuration as a dictionary compatible with both
    legacy flat calls and strict Pydantic models.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw_dict = yaml.safe_load(f) or {}

    validated_model = ExperimentConfig(**raw_dict)
    return validated_model.model_dump()
