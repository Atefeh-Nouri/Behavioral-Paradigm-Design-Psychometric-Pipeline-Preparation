# Paradigm Specification Document (PSD v1.0 FROZEN - Deliverable D1)

```
===================================================================================================
PARADIGM SPECIFICATION DOCUMENT (PSD)
Document Version: 1.0 (FROZEN)
Target Deliverable: D1
Scope: Dual-Delay AX-Continuous Performance Test (AX-CPT)
Governance: Pre-Graduate Methodological Research Portfolio | Non-Diagnostic Instrument
===================================================================================================
```

## 1. Master Architectural Specification

### 1.1 Scope & Governance
- **Research Framework**: Designed for quantitative cognitive science and psychometric modeling. Strictly non-diagnostic; does not classify clinical conditions.
- **Latent Measurement**: Recovers Sustained Attention, Inhibitory Control, and Working Memory Context Maintenance via computational models (Ex-Gaussian fitting and Hierarchical DDM).

### 1.2 Factorial Design & Block Structure
- **Total Trials**: 400 experimental trials.
- **Blocks**: 4 blocks of 100 trials each.
- **Counterbalancing**: Group A (ABBA: Short-Long-Long-Short) vs. Group B (BAAB: Long-Short-Short-Long).
- **Trial Contingencies Per Block**:
  - $AX$ (Target): 70 trials (70%). Key: `SPACE`.
  - $AY$ (Inhibition Lure): 10 trials (10%). Key: `L`.
  - $BX$ (Context Lure): 10 trials (10%). Key: `L`.
  - $BY$ (Baseline Control): 10 trials (10%). Key: `L`.

### 1.3 Chronometry & Synchronization
- Stimuli durations quantized to display refresh cycles (18 frames at 60 Hz = 300 ms).
- Delays (1200 ms vs 4000 ms) and ITIs (1000–1400 ms) scheduled via non-slip hardware clocks.
- Anticipations ($RT < 150\,\text{ms}$) categorized and isolated from decision latency modeling.
- Response window: 1000 ms clamp post-probe onset.

---

## 2. Systematic Methodological Self-Review

### 2.1 Hardware Feasibility
- Monitored display drops with watchdog threshold of 0.5 frames ($8.33\,\text{ms}$ at 60 Hz).
- Handled USB keyboard polling variance as an additive constant mapped to non-decision time ($t_0$).

### 2.2 Counterbalancing & Prepotency
- ABBA/BAAB block schedule controls time-on-task and linear fatigue interactions.
- 70% $AX$ baseline establishes strong response prepotency, ensuring $AY$ measures motor suppression and $BX$ measures context decay.

### 2.3 Computability Audit
Confirmed that every metric defined in Deliverable D1A can be derived directly from Raw Data Schema v1.0:
- Ex-Gaussian $\tau$: derived from correct $AX$ trials.
- $d'_{\text{context}}$: derived from $AX$ Hits and $BX$ False Alarms.
- $PBI$: derived from $AY$ and $BX$ error rates.
- $PES$: derived by conditioning $AX$ RT on `post_error_trial == True`.

---

## 3. Open Assumptions & Operational Constraints
1. Refresh rate locked at 60 Hz or 144 Hz (Variable refresh rates / G-Sync disabled).
2. Normal or corrected-to-normal visual acuity.
3. Attrition rule: $>15\%$ omission rate on $AX$ target trials invalidates session compliance.

```
===================================================================================================
SPECIFICATION FREEZE DECLARATION: DELIVERABLE D1 (v1.0 FROZEN)
Readiness: Specifications are frozen and sufficient for direct engine implementation.
===================================================================================================
```