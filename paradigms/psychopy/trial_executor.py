"""
State Machine Execution Engine.
Translates trial definitions into hardware flips, timing clocks,
keyboard polling, and behavioral categorization.
"""

from dataclasses import dataclass
import random
from typing import Optional

from psychopy import visual

try:
    from engine import PsychopyEngine
    from trial_logic import TrialDefinition
except ImportError:
    from .engine import PsychopyEngine
    from .trial_logic import TrialDefinition


@dataclass
class TrialResult:
    """Output metrics for a single completed trial."""
    trial_definition: TrialDefinition
    trial_index_global: int
    trial_index_block: int
    cpi_realized_ms: float
    fixation_realized_ms: float
    probe_onset_timestamp: float
    response_key: Optional[str]
    response_timestamp: Optional[float]
    rt_ms: Optional[float]
    is_correct: bool
    outcome_code: str
    is_anticipation: bool
    post_error_trial: bool
    frame_drop_detected: bool


class TrialExecutor:
    """Executes the PSD FSM for a single trial."""
    def __init__(self, engine: PsychopyEngine, config: dict):
        self.engine = engine
        self.config = config
        self.rng = random.Random()

        # Pre-render stimulus drawables to prevent dynamic allocation latency
        text_cfg = self.config["stimuli"]
        self.fixation_stim = visual.TextStim(
            self.engine.win, text="+", height=text_cfg["text_height"],
            color=text_cfg["font_color"], font=text_cfg["font"]
        )
        self.text_stim = visual.TextStim(
            self.engine.win, text="", height=text_cfg["text_height"],
            color=text_cfg["font_color"], font=text_cfg["font"]
        )

    def execute_trial(
        self,
        trial_def: TrialDefinition,
        trial_index_global: int,
        trial_index_block: int,
        is_post_error: bool
    ) -> TrialResult:
        clock_mgr = self.engine.clock_manager
        timing_cfg = self.config["timing"]
        hardware_cfg = self.config["hardware"]

        # 1. State: PRE_FIXATION (Jittered)
        fix_jitter_ms = self.rng.uniform(
            timing_cfg["fixation"]["jitter_min_ms"],
            timing_cfg["fixation"]["jitter_max_ms"]
        )
        t_fix_start, t_fix_end = self.engine.run_non_slip_interval(
            fix_jitter_ms / 1000.0, self.fixation_stim
        )
        fixation_realized_ms = (t_fix_end - t_fix_start) * 1000.0

        # 2. State: CUE_ON (Frame-quantized: 300 ms / 18 frames at 60 Hz)
        self.text_stim.text = trial_def.cue_stimulus
        cue_frames = clock_mgr.ms_to_frames(timing_cfg["stimulus"]["duration_ms"])
        t_cue_on, t_cue_off, dropped_cue = self.engine.present_stimulus_frames(
            self.text_stim, cue_frames, trial_index_global
        )

        # 3. State: DELAY (Non-slip schedule holding fixation)
        delay_s = trial_def.cpi_nominal_ms / 1000.0
        self.engine.run_non_slip_interval(delay_s, self.fixation_stim)

        # 4. State: PROBE_ON & RESPONSE_WINDOW (1000 ms clamp)
        self.text_stim.text = trial_def.probe_stimulus
        probe_frames = clock_mgr.ms_to_frames(timing_cfg["stimulus"]["duration_ms"])

        # Flush keyboard buffer immediately prior to probe flip
        self.engine.kb.clearEvents()

        t_probe_on, _, dropped_probe = self.engine.present_stimulus_frames(
            self.text_stim, probe_frames, trial_index_global
        )
        cpi_realized_ms = (t_probe_on - t_cue_on) * 1000.0

        # Await input across the remaining response window
        window_duration_s = timing_cfg["response_window_ms"] / 1000.0
        window_end_time = t_probe_on + window_duration_s

        response_key = None
        response_timestamp = None

        while clock_mgr.get_time() < window_end_time:
            keys = self.engine.kb.getKeys(
                keyList=[hardware_cfg["target_key"], hardware_cfg["non_target_key"], hardware_cfg["abort_key"]],
                waitRelease=False,
                clear=True
            )
            if keys:
                key_event = keys[0]
                if key_event.name == hardware_cfg["abort_key"]:
                    raise KeyboardInterrupt("Experiment manually aborted by operator.")
                response_key = key_event.name
                response_timestamp = key_event.rt + t_probe_on  # PTB returns rt relative to clearEvents
                break
            self.engine.win.flip()

        # 5. Outcome Scoring
        rt_ms = None
        is_anticipation = False
        anticipation_cutoff = timing_cfg["anticipation_threshold_ms"]

        if response_key is not None:
            rt_ms = (response_timestamp - t_probe_on) * 1000.0
            if rt_ms < anticipation_cutoff:
                is_anticipation = True

        if response_key is None:
            is_correct = False
            outcome_code = "OMISSION_ERROR"
        elif is_anticipation:
            is_correct = (response_key == trial_def.required_key)
            outcome_code = "ANTICIPATION"
        elif response_key == trial_def.required_key:
            outcome_code = "HIT" if trial_def.trial_type == "AX" else "CORRECT_REJECTION"
            is_correct = True
        else:
            outcome_code = "COMMISSION_ERROR"
            is_correct = False

        # 6. State: ITI (Jittered)
        iti_jitter_ms = self.rng.uniform(
            timing_cfg["iti"]["jitter_min_ms"],
            timing_cfg["iti"]["jitter_max_ms"]
        )
        self.engine.run_non_slip_interval(iti_jitter_ms / 1000.0)

        return TrialResult(
            trial_definition=trial_def,
            trial_index_global=trial_index_global,
            trial_index_block=trial_index_block,
            cpi_realized_ms=cpi_realized_ms,
            fixation_realized_ms=fixation_realized_ms,
            probe_onset_timestamp=t_probe_on,
            response_key=response_key,
            response_timestamp=response_timestamp,
            rt_ms=rt_ms,
            is_correct=is_correct,
            outcome_code=outcome_code,
            is_anticipation=is_anticipation,
            post_error_trial=is_post_error,
            frame_drop_detected=(dropped_cue or dropped_probe)
        )
