# Timing Specification, State Machine & Raw Data Schema (Day 4)

## 1. Millisecond-Level Timing Specification
Timeline of a Single AX-CPT Trial includes Fixation (400–600 ms), Cue (300 ms), Delay (1200 or 4000 ms), Probe (300 ms), and ITI (1000–1400 ms).

## 2. Trial State Machine
The state machine transitions from pre-fixation through cue, delay, probe, response window, and ITI.

## 3. System Event Codes & Raw Data Schema v1.0
The schema contains 22 columns including session_id, participant_id, trial_type, rt_ms, outcome_code, and frame_drop_detected.
