"""
Timing Verification and Hardware Benchmarking Harness (Deliverable D4 Part 1).
Quantifies display refresh stability, frame drop frequency, and input polling jitter.
"""

import sys
import numpy as np
from psychopy import visual, core
from psychopy.hardware import keyboard

PASS_THRESHOLDS = {
    "max_frame_drop_ratio": 0.001,      # Maximum 0.1% dropped frames
    "max_frame_jitter_ms": 2.0,         # Maximum 2 ms deviation from nominal frame period
    "refresh_rate_error_hz": 0.5        # Measured refresh rate must be within 0.5 Hz of nominal
}


def benchmark_display(target_hz: float = 60.0, total_test_frames: int = 1200):
    print(f"--- Running Display Refresh Benchmark ({total_test_frames} frames) ---")
    win = visual.Window(size=[800, 600], fullscr=False, color=[-1, -1, -1], waitBlanking=True)
    win.recordFrameIntervals = True

    # Warm-up phase
    for _ in range(30):
        win.flip()

    win.frameIntervals = []
    t_start = core.getTime()

    for _ in range(total_test_frames):
        win.flip()

    t_end = core.getTime()
    win.close()

    intervals = np.array(win.frameIntervals) * 1000.0  # Convert to ms
    nominal_period_ms = 1000.0 / target_hz

    effective_hz = total_test_frames / (t_end - t_start)
    drops = np.sum(intervals > (nominal_period_ms + (nominal_period_ms * 0.5)))
    drop_ratio = drops / total_test_frames
    jitter = np.std(intervals)

    print(f"Target Refresh Rate:    {target_hz:.2f} Hz ({nominal_period_ms:.3f} ms)")
    print(f"Measured Refresh Rate:  {effective_hz:.2f} Hz")
    print(f"Frame Jitter (StdDev):  {jitter:.3f} ms")
    print(f"Dropped Frames:         {drops} / {total_test_frames} ({drop_ratio * 100:.2f}%)")

    assert abs(effective_hz - target_hz) <= PASS_THRESHOLDS["refresh_rate_error_hz"], \
        f"FAILED: Refresh rate deviation exceeds {PASS_THRESHOLDS['refresh_rate_error_hz']} Hz"
    assert drop_ratio <= PASS_THRESHOLDS["max_frame_drop_ratio"], \
        f"FAILED: Frame drop ratio ({drop_ratio:.4f}) exceeds threshold ({PASS_THRESHOLDS['max_frame_drop_ratio']})"
    assert jitter <= PASS_THRESHOLDS["max_frame_jitter_ms"], \
        f"FAILED: Frame jitter ({jitter:.2f} ms) exceeds threshold ({PASS_THRESHOLDS['max_frame_jitter_ms']} ms)"

    print(">> DISPLAY BENCHMARK: PASSED <<\n")


def benchmark_keyboard_jitter(iterations: int = 100):
    print(f"--- Running Keyboard Polling Latency Benchmark ({iterations} iterations) ---")
    kb = keyboard.Keyboard(backend="ptb")
    clock = core.MonotonicClock()

    delays = []
    for _ in range(iterations):
        t0 = clock.getTime()
        kb.clearEvents()
        t1 = clock.getTime()
        delays.append((t1 - t0) * 1000.0)
        core.wait(0.005)

    delays = np.array(delays)
    print(f"Mean Polling Execution: {np.mean(delays):.4f} ms")
    print(f"Max Polling Execution:  {np.max(delays):.4f} ms")
    assert np.max(delays) < 1.0, "FAILED: Keyboard event clearing exceeds 1.0 ms overhead."
    print(">> KEYBOARD BENCHMARK: PASSED <<\n")


if __name__ == "__main__":
    try:
        benchmark_display(target_hz=60.0)
        benchmark_keyboard_jitter()
        print("ALL TIMING AND HARDWARE QA VERIFICATIONS PASSED.")
    except AssertionError as e:
        print(str(e))
        sys.exit(1)
