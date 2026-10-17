# Timing Verification & Operator Quality Assurance Protocol (Deliverable D4 Part 1)

## 1. Automated Verification Script (`tests/verify_timing.py`)
- **Display Benchmark**: Measures frame intervals across 1200 flips.
  - Thresholds: Refresh rate error $\le 0.5\,\text{Hz}$, frame drop ratio $\le 0.001$ ($0.1\%$), frame jitter $\le 2.0\,\text{ms}$.
- **Keyboard Latency Benchmark**: Asserts Psychtoolbox event clearing overhead is $<1.0\,\text{ms}$.

## 2. Pre-Flight Manual Operator Checklist
```text
===================================================================================================
EXPERIMENTAL PRE-FLIGHT QUALITY ASSURANCE PROTOCOL
===================================================================================================
Hardware Setup & Environmental Checks:
  [ ] 1. DISPLAY SETTINGS: Verify refresh rate is set to exactly 60.00 Hz or 144.00 Hz.
         Variable refresh rate (G-Sync/FreeSync) MUST be disabled.
  [ ] 2. BACKGROUND PROCESSES: Terminate browsers, cloud sync, and background apps.
         Set OS Power Plan to "High Performance".
  [ ] 3. KEYBOARD SETUP: Connect keyboard to a rear USB root hub (avoid unpowered hubs/Bluetooth).
  [ ] 4. OS NOTIFICATIONS: Turn on "Do Not Disturb". Disable display sleep and screen savers.

Verification Script Execution:
  [ ] 5. Run: python tests/verify_timing.py
  [ ] 6. Confirm message: "ALL TIMING AND HARDWARE QA VERIFICATIONS PASSED".
  [ ] 7. Inspect measured frame jitter (must be < 2.0 ms).

Session Initiation:
  [ ] 8. Launch session: python paradigms/psychopy/main.py --participant PXXX --group [A|B]
  [ ] 9. Verify participant passes criterion practice before main blocks begin.
===================================================================================================
```

## 3. Timing Diagnostic Guide
- **Frame Drops $>0.1\%$**: Disable OS compositor (transparent windows, game overlays), force exclusive fullscreen.
- **Refresh Mismatch**: Adjust display refresh rate in OS graphics settings to match config target.
- **Keyboard Jitter $>2\,\text{ms}$**: Verify Psychtoolbox installation (`pip install psychtoolbox`); use wired USB port.