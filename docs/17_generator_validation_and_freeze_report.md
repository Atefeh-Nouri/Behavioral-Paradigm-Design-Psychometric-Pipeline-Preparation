# Generator Validation & Benchmark Freeze Report (Deliverable D5 Part 2)

## 1. Statistical Recovery & Contrast Verification

### 1.1 Parameter Recovery Evaluation ($N = 49$ Compliant Subjects)
- **Lapse Parameter ($\tau$ Recovery)**: True $\tau_i$ correlated with empirical latency tail proxy ($RT_{90\text{th}} - RT_{50\text{th}}$ on correct $AX$ trials).
  - *Result*: Pearson $r = 0.912$ ($p < 0.001$). Confirms accurate translation of latent $\tau$ into empirical tails.
- **Sensorimotor Central Latency ($\mu$ Recovery)**: True $\mu_i$ correlated with median RT ($RT_{50\text{th}}$).
  - *Result*: Pearson $r = 0.941$ ($p < 0.001$).
- **Context Discriminability ($d'$ Recovery)**: True $d'_i$ correlated with empirical Hautus-corrected $d'$.
  - *Result*: Pearson $r = 0.884$ ($p < 0.001$).

### 1.2 Contrast Effect Size Verification
- **Conflict Slowing ($AY$ vs. $AX$)**:
  - Mean $AX$ RT: $468.2\,\text{ms}$ ($SD = 36.1$).
  - Mean $AY$ RT: $534.8\,\text{ms}$ ($SD = 41.2$).
  - *Observed Contrast*: $+66.6\,\text{ms}$ slowing ($t(48) = 14.82, p < 0.001$, Cohen's $d = 1.72$). Matches target $+65.0\,\text{ms}$.
- **Context Degradation under Working Memory Load ($BX$ Errors)**:
  - Short Delay ($1200\,\text{ms}$): Mean Error Rate $= 6.1\%$ ($SD = 3.8\%$).
  - Long Delay ($4000\,\text{ms}$): Mean Error Rate $= 23.4\%$ ($SD = 7.2\%$).
  - *Observed Contrast*: $+17.3\%$ increase in commission errors across delay ($t(48) = 16.11, p < 0.001$).
- **Time-on-Task Vigilance Drift**:
  - Block 1 Mean RT: $452.1\,\text{ms} \to$ Block 4 Mean RT: $484.9\,\text{ms}$ ($+32.8\,\text{ms}$ linear drift).

### 1.3 Stress-Test Case Audit (Subject 50)
- $AX$ Omission Rate: $18.2\%$ (exceeds $15.0\%$ compliance threshold).
- Global $d'$: $0.24$ (near chance).
- *Result*: Successfully triggers compliance exclusion filter.

---

## 2. Deliverable D5 Freeze Declaration

```
===================================================================================================
BENCHMARK DATASET FREEZE DECLARATION: DELIVERABLE D5
===================================================================================================
Dataset Identifier: AX-CPT Synthetic Benchmark v1.0
Total Subject Records: 50 participants (49 compliant, 1 non-compliant stress case)
Total Trial Observations: 19,974 validly ingested rows
Validation Status: APPROVED & FROZEN
Core Properties Verified:
  - Ex-Gaussian skewness and right-tail latency confirmed.
  - Parameter recovery correlations: r(tau) = 0.912, r(mu) = 0.941, r(d') = 0.884.
  - Conflict slowing on AY trials confirmed (+66.6 ms, p < 0.001).
  - Context degradation on BX trials confirmed (6.1% to 23.4% error jump, p < 0.001).
===================================================================================================
```