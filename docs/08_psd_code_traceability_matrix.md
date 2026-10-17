# PSD v1.0 to Code Traceability Matrix (Day 8)

| PSD v1.0 Section | Functional Requirement | Implementing Python Module | Class / Method |
| :--- | :--- | :--- | :--- |
| **Section 1.2** | Factorial cell balancing (70/10/10/10) | `paradigms/psychopy/trial_logic.py` | `TrialSequenceGenerator.generate_block()` |
| **Section 1.2** | Run-rules (Max 4 AX, Max 2 Non-Target) | `paradigms/psychopy/trial_logic.py` | `TrialSequenceGenerator._satisfies_run_rules()` |
| **Section 1.2** | Counterbalancing (ABBA / BAAB) | `paradigms/psychopy/main.py` | Block loop scheduler |
| **Section 1.3** | State Machine & Response Chronometry | `paradigms/psychopy/trial_executor.py` | `TrialExecutor.execute_trial()` |
| **Section 1.3** | Anticipation isolation ($RT < 150\,\text{ms}$) | `paradigms/psychopy/trial_executor.py` | `TrialExecutor.execute_trial()` scoring |
| **Section 2.5** | Criterion-gated practice & calibration | `paradigms/psychopy/ui.py` | `PracticeManager.run_practice()` |
| **Section 4.2** | Raw Data Schema v1.0 Output | `paradigms/psychopy/logger.py` | `SessionDataLogger.log_trial()` |