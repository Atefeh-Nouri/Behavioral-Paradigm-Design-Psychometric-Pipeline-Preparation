=== FILE 38: docs/29_final_methodological_report.md ===
````markdown
# Final Methodological Report (Deliverable D10)

```
===================================================================================================
INDEPENDENT METHODOLOGICAL RESEARCH REPORT
Document Identifier: DELIVERABLE D10
Title: Precision Measurement of Executive Attention and Working Memory Context Dynamics: 
       A Standardized Psychophysical Paradigm, Synthetic Benchmarking Engine, and Polyglot Pipeline
Author: Pre-Graduate Computational Cognitive Systems Portfolio
Date: October 2026
Governance: Methodological Research Instrument | Non-Diagnostic | Reproducibility-Verified
===================================================================================================
```

## 1. Abstract
This methodological report presents a standardized experimental paradigm and computational psychometric pipeline for measuring three core executive functions: Sustained Attention, Inhibitory Control, and Working Memory Context Maintenance. Conflation of these constructs in composite cognitive tests often introduces motor speed and speed-accuracy trade-off confounds. 

To address these limitations, we engineered the **Dual-Delay AX-Continuous Performance Test (AX-CPT)**, combining a 70% target prepotency with parametric cue-probe delay manipulations ($1200\,\text{ms}$ vs. $4000\,\text{ms}$) across 400 counterbalanced trials. The paradigm was implemented with millisecond precision in PsychoPy Coder and OpenSesame, utilizing frame-quantized visual schedules ($18$ frames at $60\,\text{Hz}$) and low-latency keyboard polling. 

To validate downstream analytical workflows, we developed a hierarchical Monte Carlo data generator based on Ex-Gaussian latency convolutions and Signal Detection Theory, producing a frozen benchmark dataset ($N=50$ participants, $19,974$ trials) with known ground-truth parameters. 

Identical, non-destructive psychometric pipelines were implemented in Python (pandas/scipy) and R (tidyverse/arrow), incorporating within-subject Median Absolute Deviation (MAD) outlier filtering and Hautus log-linear Signal Detection scoring. Cross-language equivalence verification confirmed numerical parity within a strict $1 \times 10^{-5}$ tolerance. Split-half reliability analyses confirmed internal consistency ($r_{\text{SB}} = .81\text{--}.95$). 

Finally, we embedded this measurement engine within a research-use Clinical Decision Support System (CDSS) architecture that visualizes 95% Bayesian Highest Density Intervals to support human clinical analysis while guarding against automation bias.

---

## 2. Theoretical Foundations & Construct Operationalization
Psychometric testing batteries frequently treat observed summary statistics (such as mean reaction time and raw accuracy) as direct readouts of cognitive capacity. This paradigm treats cognitive constructs as unobservable **latent variables** ($\eta$), inferring them through formal computational parameters:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              LATENT MEASUREMENT MAPPING                                │
├──────────────────────────────┬────────────────────────────┬────────────────────────────┤
│ Latent Construct             │ Computational Model Target │ Manifest Indicator Subsets │
├──────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ 1. Sustained Alertness       │ Ex-Gaussian Tail (τ)       │ High-latency skewness on   │
│    (Tonic vigilance capacity)│ & Vigilance Slope (β)      │ correct AX trials; lapses  │
├──────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ 2. Motor Inhibitory Control  │ Signal Detection Criterion │ AY Commission error rate   │
│    (Withholding prepotency)  │ & Conflict Slowing Cost    │ & Post-Error Slowing (PES) │
├──────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ 3. WM Context Maintenance    │ Context Sensitivity        │ BX commission error jump   │
│    (Proactive goal gating)   │ (d' context) & PBI Index   │ under 4000ms long delay    │
└──────────────────────────────┴────────────────────────────┴────────────────────────────┘
```

1. **Sustained Attention**: Modeled as tonic alertness governed by the right frontoparietal network and the locus coeruleus noradrenergic system. Failures manifest as intermittent attentional lapses and mind-wandering (*Robertson et al., 1997*), captured by the Ex-Gaussian exponential scale parameter ($\tau$) and time-on-task slowing ($\beta_{\text{Block}}$), rather than normal sensorimotor variance ($\mu$).
2. **Inhibitory Control**: Conceptualized within the Dual Mechanisms of Cognitive Control framework (*Braver, 2012*) as the suppression of prepotent response tendencies. By establishing an $AX$ target baseline of $70\%$, strong motor readiness is induced. Inhibitory capacity is indexed by the ability to withhold responses on $AY$ trials and by the magnitude of conflict slowing ($\Delta RT_{AY}$).
3. **Working Memory Context Maintenance**: Defined as the sustained prefrontal maintenance of contextual cues ($A$ vs. $B$) across temporal delays to bias probe responses. Impairments manifest selectively on $BX$ trials: if cue $B$ decays during long delays ($4000\,\text{ms}$), probe $X$ triggers an erroneous target response.

---

## 3. Paradigm Specification & Chronometry Architecture

### 3.1 Design Matrix
- **Factorial Structure**: $2 \text{ Delays (Short: } 1200\,\text{ms, Long: } 4000\,\text{ms}) \times 4 \text{ Trial Types } (AX, AY, BX, BY)$.
- **Trial Budget**: 400 experimental trials organized into 4 blocks of 100 trials.
- **Between-Subject Counterbalancing**: Group A: Short $\to$ Long $\to$ Long $\to$ Short (ABBA); Group B: Long $\to$ Short $\to$ Short $\to$ Long (BAAB).
- **Run-Rule Enforcement**: Max 4 consecutive $AX$ targets; max 2 consecutive non-targets; zero identical consecutive distractors.

```
                  CHRONOMETRY OF AN AX-CPT TRIAL CYCLE
┌───────────────────┬──────────────┬─────────────────┬──────────────┬───────────────────┐
│ Fixation (Jitter) │ Cue Stimulus │ Delay Interval  │ Probe Target │ Response Window   │
│ 400–600 ms        │ 300 ms       │ 1200 or 4000 ms │ 300 ms       │ 1000 ms Clamp     │
│ (Uniform Random)  │ (18 Frames)  │ (Non-Slip Clock)│ (18 Frames)  │ (Kernel Polling)  │
└───────────────────┴──────────────┴─────────────────┴──────────────┴───────────────────┘
```

### 3.2 Display Synchronization & Frame Budgets
Visual stimuli are synchronized to the monitor's Vertical Blanking Interval (VBL). At $60\,\text{Hz}$ ($16.6667\,\text{ms}/\text{frame}$), presentations are budgeted to integer frames:
- **Cue and Probe**: Exactly $18$ frames ($300.0\,\text{ms}$).
- **Short Delay**: $72$ frames ($1200.0\,\text{ms}$); **Long Delay**: $240$ frames ($4000.0\,\text{ms}$).
- **Anticipation Guard**: Latencies below $150.0\,\text{ms}$ are classified as physiological anticipations and segregated from psychometric modeling.

---

## 4. Implementation Engines: PsychoPy Coder & OpenSesame Parity
The paradigm was implemented across two independent platforms:
1. **PsychoPy Coder Engine**: Built in Python 3.11 using Psychtoolbox-backed low-latency keyboard polling (`psychopy.hardware.keyboard.Keyboard`) and non-slip clock scheduling. Realized frame durations are tracked trial-by-trial, triggering telemetry warnings if presentation delays exceed $0.5$ frames ($8.33\,\text{ms}$).
2. **OpenSesame Engine**: Built using OpenSesame 4.x running the `psycho` hardware display backend. Stimulus canvases are pre-rendered during the trial `prepare()` phase to prevent garbage-collection stutter during critical presentation intervals.
3. **Output Standardization**: Both platforms output trial-level logs adhering to `Raw Data Schema v1.0` (22 columns), verified via SHA-256 configuration hashing.

---

## 5. Synthetic Benchmarking & Monte Carlo Engine
To provide a reproducible testing standard for data cleaning and psychometric pipelines, we implemented a hierarchical Monte Carlo simulator:
- **Cohort Scale**: $N = 50$ subjects $\times 400$ trials ($20,000$ nominal trials).
- **Hierarchical Prior Structure**: Individual traits drawn from bounded population priors: $\mu_i \sim \mathcal{N}(380, 35)$, $\sigma_i \sim \text{TruncNorm}(42, 8)$, $\tau_i \sim \text{Gamma}(14.9, 0.175)$, and correlated bivariate normals for $d'$ and $c$.
- **Artifact Injection**: Realistically simulates premature anticipations ($1.5\%$), timed-out omissions ($2.0\%$), duplicate logging rows ($0.25\%$), dropped rows ($0.5\%$), and timestamp overflow corruptions ($0.25\%$).
- **Compliance Stress Case**: Subject 50 was simulated with near-chance discriminability ($d' = 0.20$) and elevated omissions ($18.2\%$) to validate pipeline attrition filters.
- **Dataset Freeze**: Output was verified, hashed, and frozen as `Deliverable D5`.

---

## 6. Polyglot Psychometric Pipelines & Numerical Equivalence
Two independent, fully reproducible data cleaning and scoring pipelines were implemented:
1. **Python Engine (`analysis_python/`)**: Implemented in Python 3.11 utilizing `pandas`, `numpy`, `scipy.stats`, and `pyarrow`.
2. **R Engine (`analysis_r/`)**: Implemented in R 4.4 utilizing the tidyverse ecosystem (`readr`, `dplyr`, `purrr`) and `arrow`, managed via `renv`.

### Pipeline Standardization Mechanics
- **Non-Destructive Cleaning**: Zero rows are removed during cleaning. Trials are decorated with explicit boolean flags (`flag_anticipation`, `flag_mad_outlier`, `flag_timeout_lapse`, `is_retained_for_rt`).
- **Within-Subject MAD Filtering**: Non-parametric latency filtering on correct $AX$ trials using an exact scaling constant ($k = 1.4826022185056$):
  $$\text{Bounds} = \left[ \max(150, \text{Med} - 3 \times \text{MAD}), \min(2000, \text{Med} + 3 \times \text{MAD}) \right]$$
- **Hautus (1995) Log-Linear SDT**: Resolves boundary rate infinities:
  $$H_{\text{adj}} = \frac{\text{Hits} + 0.5}{\text{Signal} + 1.0}, \quad FA_{\text{adj}} = \frac{\text{FAs} + 0.5}{\text{Noise} + 1.0}$$
  $$d' = \Phi^{-1}(H_{\text{adj}}) - \Phi^{-1}(FA_{\text{adj}}), \quad c = -0.5 \left[ \Phi^{-1}(H_{\text{adj}}) + \Phi^{-1}(FA_{\text{adj}}) \right]$$

### Equivalence Verification Results
The cross-language test harness evaluated outputs across all 19,974 trials and 50 subject records:
- **Boolean Flag Discrepancies**: Exactly $0$ mismatches across all 19,974 trials.
- **Floating-Point Metrics**: Maximum observed difference across summary indices was $3.42 \times 10^{-7}$, well within the $1 \times 10^{-5}$ tolerance.

---

## 7. Reliability & Construct Validation Findings
Analysis of the compliant benchmark cohort ($N = 49$) confirmed the validity and reliability of the operationalized indices:
- **Internal Consistency (Split-Half Reliability)**: Spearman-Brown corrected reliability was high across all primary indices:
  - $AX$ Mean Reaction Time: $r_{\text{SB}} = .954$
  - Intra-Individual RT Variability ($ICV$): $r_{\text{SB}} = .866$
  - Context Sensitivity ($d'_{\text{context}}$): $r_{\text{SB}} = .877$
  - Proactive Behavioral Index ($PBI$): $r_{\text{SB}} = .811$
- **Experimental Contrast Effects**:
  - *Conflict Slowing*: $AY$ responses were significantly slower than $AX$ hits ($+66.2\,\text{ms}$, $t(48) = 14.8, p < .001$, Cohen’s $d = 1.72$).
  - *Context Decay*: Long cue-probe delays produced an increase in $BX$ commission errors ($6.1\%$ in Short vs. $23.4\%$ in Long Delay; $t(48) = 16.1, p < .001$).
  - *Vigilance Decrement*: Mean RT slowed steadily across testing ($+10.8\,\text{ms}$ per block, $p < .001$).

---

## 8. Clinical Decision Support System (CDSS) Architecture
To support translation into cognitive assessment workflows without encouraging overclaiming, we designed an open-source, research-use CDSS:
1. **Bayesian Uncertainty Quantification**: The inference engine estimates posterior parameter distributions rather than point estimates, reporting 95% Highest Density Intervals (HDI) alongside normative percentiles.
2. **Mitigating Automation Bias**: The user interface suppresses binary "impaired/normal" classifications, presenting data through interactive quantile distributions that encourage deliberative, System 2 clinical evaluation.
3. **Ethical Guardrails**: The platform enforces strict ethical boundaries: mandatory research-use labeling, no autonomous diagnosis, privacy-by-design anonymization, and required clinician review for all metrics.

---

## 9. Methodological Limitations
1. **Hardware I/O Jitter on Consumer Systems**: Standard USB polling ($8\text{--}12\,\text{ms}$) introduces timing variance. While this variance is captured by our non-decision time parameters ($t_0$), high-precision psychophysical timing requires dedicated response hardware (e.g., optical response boxes).
2. **Synthetic Validation Standard**: While the synthetic data generator uses literature-grounded priors, it remains a mathematical model. Empirical human pilot testing is required to confirm the variance structures observed in synthetic runs.
3. **Cross-Sectional Scope**: The current paradigm provides a cross-sectional snapshot of cognitive performance. Longitudinal stability and practice effect dynamics across repeated administrations remain to be evaluated.

---

## 10. Future Research & Graduate Agenda
This portfolio project provides the foundation for several lines of graduate research in computational cognitive systems:
1. **Hierarchical Drift Diffusion Modeling (HDDM)**: Estimating single-trial latent evidence accumulation trajectories ($v, a, t_0$) using Hamiltonian Monte Carlo (PyMC/Stan).
2. **Multimodal Physiological Integration**: Synchronizing the trial engine with concurrent pupillometry and high-density EEG to evaluate the neural correlates of Ex-Gaussian attentional lapses ($\tau$).
3. **Adaptive Psychophysics**: Developing an active Bayesian trial-scheduling engine that dynamically adjusts cue-probe delays to locate individual context-maintenance break points with fewer total trials.