"""
Core Psychophysical Timing and Hardware Engine.
Handles V-Sync synchronization, frame-accurate presentation,
non-slip interval accounting, and dropped frame detection.
"""

from dataclasses import dataclass
import logging
from typing import List, Optional, Tuple
from psychopy import core, visual
from psychopy.hardware import keyboard

logger = logging.getLogger("TimingEngine")


@dataclass
class FrameDropEvent:
    """Telemetry payload for frame-drop detection."""
    trial_index: int
    expected_duration_ms: float
    actual_duration_ms: float
    dropped_delta_ms: float
    timestamp: float


class EngineClockManager:
    """
    Manages non-slip timing clocks and converts millisecond specifications
    into exact display refresh frames.
    """
    def __init__(self, refresh_rate_hz: float):
        self.refresh_rate_hz = refresh_rate_hz
        self.frame_period_s = 1.0 / refresh_rate_hz
        self.frame_period_ms = self.frame_period_s * 1000.0
        self.master_clock = core.MonotonicClock()

    def ms_to_frames(self, duration_ms: float) -> int:
        """Converts millisecond duration to integer display frames using standard rounding."""
        return int(round(duration_ms / self.frame_period_ms))

    def get_time(self) -> float:
        """Returns high-resolution monotonic time in seconds."""
        return self.master_clock.getTime()


class PsychopyEngine:
    """
    Encapsulates the PsychoPy Window, hardware inputs, and frame-budget watchdog.
    """
    def __init__(self, config: dict):
        self.config = config
        self.win: Optional[visual.Window] = None
        self.kb: Optional[keyboard.Keyboard] = None
        self.clock_manager: Optional[EngineClockManager] = None
        self.frame_drop_records: List[FrameDropEvent] = []
        self._measured_refresh_rate: float = 0.0

    def initialize_hardware(self) -> None:
        """Initializes display context, validates refresh rate, and hooks low-latency keyboard."""
        env_cfg = self.config["environment"]

        # Configure Psychtoolbox-backed low-latency keyboard
        self.kb = keyboard.Keyboard(backend=self.config["hardware"]["keyboard_backend"])

        # Initialize exclusive visual context
        self.win = visual.Window(
            size=env_cfg["window_resolution"],
            fullscr=env_cfg["fullscreen"],
            screen=env_cfg["screen_number"],
            color=env_cfg["background_color"],
            units=env_cfg["units"],
            allowGUI=env_cfg["allow_gui"],
            waitBlanking=True  # Force V-Sync synchronization
        )
        self.win.mouseVisible = env_cfg["cursor_visible"]
        self.win.recordFrameIntervals = True

        # Detect and validate hardware refresh rate
        measured_hz = self.win.getActualFrameRate(
            nIdentical=10,
            nWarmUpFrames=10,
            nMaxFrames=60
        )
        if measured_hz is None:
            logger.warning("Could not detect hardware refresh rate. Falling back to config target.")
            measured_hz = env_cfg["target_refresh_hz"]

        self._measured_refresh_rate = float(measured_hz)
        target_hz = env_cfg["target_refresh_hz"]
        tolerance = env_cfg["refresh_tolerance_hz"]

        if abs(self._measured_refresh_rate - target_hz) > tolerance:
            raise RuntimeError(
                f"Display refresh rate mismatch! Target: {target_hz} Hz, "
                f"Measured: {self._measured_refresh_rate:.2f} Hz. Tolerable delta: {tolerance} Hz."
            )

        self.clock_manager = EngineClockManager(self._measured_refresh_rate)
        logger.info(
            "Hardware engine online. Refresh Rate: %.2f Hz (Frame budget: %.3f ms)",
            self._measured_refresh_rate,
            self.clock_manager.frame_period_ms
        )

    def present_stimulus_frames(
        self,
        stimulus_drawable,
        duration_frames: int,
        trial_index: int
    ) -> Tuple[float, float, bool]:
        """
        Presents a visual stimulus for a precise number of display frames.
        Returns (onset_timestamp, offset_timestamp, frame_dropped_flag).
        """
        assert self.win is not None
        assert self.clock_manager is not None

        frame_period = self.clock_manager.frame_period_s
        expected_duration = duration_frames * frame_period

        stimulus_drawable.draw()
        onset_time = self.win.flip()

        # Maintain presentation across remaining frame cycles
        for _ in range(duration_frames - 1):
            stimulus_drawable.draw()
            self.win.flip()

        # Clear stimulus on subsequent flip
        offset_time = self.win.flip()
        realized_duration = offset_time - onset_time

        # Watchdog: threshold is 0.5 frames of slippage
        dropped_delta = realized_duration - expected_duration
        is_dropped = dropped_delta > (frame_period * 0.5)

        if is_dropped:
            record = FrameDropEvent(
                trial_index=trial_index,
                expected_duration_ms=expected_duration * 1000.0,
                actual_duration_ms=realized_duration * 1000.0,
                dropped_delta_ms=dropped_delta * 1000.0,
                timestamp=onset_time
            )
            self.frame_drop_records.append(record)
            logger.warning(
                "Trial %d: Dropped frame detected! Expected: %.2f ms, Got: %.2f ms (Delta: +%.2f ms)",
                trial_index, record.expected_duration_ms, record.actual_duration_ms, record.dropped_delta_ms
            )

        return onset_time, offset_time, is_dropped

    def run_non_slip_interval(self, duration_s: float, background_drawable=None) -> Tuple[float, float]:
        """
        Executes a continuous interval without accumulating temporal drift,
        optionally rendering a persistent fixation marker.
        """
        assert self.win is not None
        start_time = self.clock_manager.get_time()
        end_time = start_time + duration_s

        while self.clock_manager.get_time() < end_time:
            if background_drawable is not None:
                background_drawable.draw()
            self.win.flip()

        terminal_time = self.clock_manager.get_time()
        return start_time, terminal_time

    def close(self) -> None:
        """Gracefully release hardware handles."""
        if self.win:
            self.win.close()
            core.quit()
