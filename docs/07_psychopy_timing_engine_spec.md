# PsychoPy Core Timing Architecture & Precision Trade-offs (Day 7)

## 1. Psychophysical Bottlenecks & Design Solutions

1. **Vertical Blanking Interval (VBL) Synchronization**:
   - Stimulus onset is locked to display refresh cycles via `win.flip()`.
   - Prevents visual tearing and guarantees quantized presentation durations (e.g., exactly 18 frames at 60 Hz for 300 ms).
2. **Clock Drift vs. Frame Counting**:
   - Pure `time.sleep()` drifts due to OS scheduling preemption.
   - Frame counting without clocks can lead to time expansion if frames drop.
   - *EngineClockManager* uses frame-based flips for brief visual stimuli (Cue, Probe) and non-slip monotonic timers (`core.MonotonicClock`) for intervals (Delay, ITI).
3. **Low-Latency Keyboard Hooks**:
   - Uses `psychopy.hardware.keyboard.Keyboard` backed by Psychtoolbox.
   - Bypasses OS event polling to register kernel-level hardware timestamps.

## 2. Frame-Drop Watchdog
- Compares realized duration against expected frame budget.
- Slippage $>0.5$ frames ($>8.33\,\text{ms}$ at 60 Hz) logs a `FrameDropEvent` telemetry record.