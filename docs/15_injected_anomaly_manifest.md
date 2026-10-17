# Injected Anomaly Manifest & Pipeline Test Contract (Day 15)

## 1. Overview
To ensure robust validation of downstream cleaning pipelines (Phases 4 and 5), the synthetic data generator injects controlled biological artifacts, technical hardware glitches, and a non-compliant stress case.

## 2. Injected Anomaly Registry

| Anomaly Identifier | Target Layer | Injection Mechanism / Rate | Physical / Biological Cause | Required Cleaning Pipeline Response |
| :--- | :--- | :--- | :--- | :--- |
| **ANOM-01: Premature Anticipation** | Trial RT | $RT \sim \text{Uniform}(60, 145)\,\text{ms}$;<br>Rate: $\approx 1.5\%$ per subject. | Guessing, rhythmic motor entrainment before visual decoding. | Tag `is_anticipation = True`; censor from Ex-Gaussian and DDM parameter estimation. |
| **ANOM-02: Timeout Lapse** | Trial RT | Ex-Gaussian draw exceeds $1000\,\text{ms}$;<br>Rate: $\approx 2.0\%$. | Severe attentional lapse, micro-sleep, mind-wandering. | Retain as `OMISSION_ERROR`; include in vigilance decrement tracking; exclude from RT shape fitting. |
| **ANOM-03: Dropped Trials** | Schema / Rows | Pseudorandom deletion of $2$ trials per session ($0.5\%$). | USB I/O failure, thread preemption, operating system file lock. | Flag gap in `trial_index_global` sequence; log warning; do not shift remaining trial counters. |
| **ANOM-04: Duplicated Trial Rows** | Schema / Rows | Duplication of $1$ trial per session ($0.25\%$). | Socket re-transmission or logging retry loop. | Identify duplicate `trial_index_global`; drop redundant row using `drop_duplicates(subset=['trial_index_global'])`. |
| **ANOM-05: Corrupt RT Values** | Schema / Data | Injection of $RT = -99.0\,\text{ms}$ or $RT > 10000\,\text{ms}$ ($0.25\%$). | Sensor timer overflow, bit-flip, or clock uncoupling. | Range validation assertion: drop or set to `null` if $RT < 0$ or $RT > 2000\,\text{ms}$. |
| **ANOM-06: Near-Chance Subject** | Subject / Trait | Subject 50: $d' = 0.20$, $\tau = 320\,\text{ms}$, Omissions $= 18\%$. | Severe non-compliance, intoxication, sleep onset, or task refusal. | Attrition filter: exclude subject entirely because $AX$ omission rate exceeds the $15\%$ threshold. |