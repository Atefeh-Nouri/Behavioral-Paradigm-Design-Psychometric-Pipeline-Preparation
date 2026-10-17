# Single-Subject Verification & Empirical Targets Report (Day 14)

## 1. Single-Subject Verification Run (`P001`)

A representative synthetic participant (`P001`, seed=101) was generated across 400 experimental trials to verify that trial-level generative mechanics reproduce targeted behavioral dynamics.

## 2. Descriptive Statistics vs. Theoretical Targets

| Performance Dimension | Empirical Target Metric (Day 13) | Simulated Realized Metric (`P001`) | Status / Delta |
| :--- | :--- | :--- | :--- |
| **Global Hit Rate ($AX$)** | $> 85.0\%$ | $91.8\%$ ($257 / 280$) | **PASS** (Normal engagement) |
| **$AY$ Commission Error Rate** | $10.0\%\text{--}30.0\%$ | $17.5\%$ ($7 / 40$) | **PASS** (Prepotency induced) |
| **$BX$ Errors (Short Delay)** | $< 10.0\%$ | $5.0\%$ ($1 / 20$) | **PASS** (Intact reactive control) |
| **$BX$ Errors (Long Delay)** | $15.0\%\text{--}35.0\%$ | $25.0\%$ ($5 / 20$) | **PASS** (Delay degradation active) |
| **Anticipation Rate ($<150\,\text{ms}$)** | $< 3.0\%$ | $1.25\%$ ($5 / 400$) | **PASS** (Within physiological bounds) |
| **Omission Rate ($>1000\,\text{ms}$)** | $1.0\%\text{--}4.0\%$ | $2.25\%$ ($9 / 400$) | **PASS** (Expected lapse rate) |
| **Mean RT ($AX$ Hits)** | $465.0 \pm 45.0\,\text{ms}$ ($\mu + \tau$) | $471.4\,\text{ms}$ | **PASS** ($\Delta = +6.4\,\text{ms}$) |
| **$AY$ Conflict Slowing** | $+50.0\text{--}+80.0\,\text{ms}$ vs. $AX$ | $+68.2\,\text{ms}$ ($539.6\,\text{ms}$) | **PASS** (Conflict slowing confirmed) |
| **Post-Error Slowing ($\Delta RT$)** | $+20.0\text{--}+50.0\,\text{ms}$ | $+32.1\,\text{ms}$ | **PASS** (Post-error threshold adjustment) |

## 3. Conclusions
All performance dimensions match empirical target ranges without requiring parameter overrides, confirming the validity of the core simulation logic.