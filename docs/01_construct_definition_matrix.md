# Construct Deconstruction & Measurement Operationalization (Day 1)

## 1. Latent Constructs Deconstruction

### 1.1 Sustained Attention (Vigilance & Tonic Alertness)
- **Theoretical Framework**: Governed by the endogenous capacity to maintain an alert, goal-directed processing state across extended temporal intervals without external prompting (*Parasuraman et al., 1998*). Supported neuroanatomically by a predominantly right-lateralized frontoparietal network with ascending noradrenergic projections from the locus coeruleus (*Aston-Jones & Cohen, 2005*).
- **Core Failure Modes**:
  1. *Resource Depletion*: Processing capacity degrades monotonically as a function of continuous energetic expenditure (*Warm, Parasuraman, & Matthews, 2008*).
  2. *Mind-Wandering / DMN Intrusion*: Inability to suppress task-unrelated thoughts (TUTs), leading to periodic sensory attenuation and attentional lapses (*Robertson et al., 1997*; *Weissman et al., 2006*).
- **Canonical Paradigms**: Conners CPT, Sustained Attention to Response Task (SART), Psychomotor Vigilance Task (PVT), Mackworth Clock.
- **Observed Manifest Indicators**: Ex-Gaussian exponential tail ($\tau$), intra-individual coefficient of variation ($ICV = SD_{\text{RT}} / M_{\text{RT}}$), omission error rate (misses), linear RT drift across blocks ($\beta_{\text{Block}}$), anticipations ($RT < 150\,\text{ms}$).

---

### 1.2 Selective & Inhibitory Attentional Control
- **Theoretical Framework**: Encompasses processes that suppress prepotent, automatic, or task-irrelevant impulses, mental representations, or behavioral actions (*Miyake et al., 2000*; *Diamond, 2013*).
- **Mechanisms**:
  1. *Action Cancellation (Response Inhibition)*: Halting an already initiated motor command, formalized by the Independent Horse-Race Model (*Logan & Cowan, 1984*). Subserved by right inferior frontal cortex (rIFC), pre-SMA, and the subthalamic nucleus (STN) hyperdirect pathway.
  2. *Interference / Conflict Resolution*: Resolving competing perceptual/motor representations (*Botvinick et al., 2001*), governed by anterior cingulate cortex (ACC) and dorsolateral prefrontal cortex (DLPFC).
- **Canonical Paradigms**: Go/No-Go (GNG), Stop-Signal Task (SST), Eriksen Flanker, Stroop.
- **Observed Manifest Indicators**: Commission errors on withhold trials (false alarms), Stop-Signal Reaction Time (SSRT), conflict interference slowing ($\Delta RT_{\text{Conflict}}$), Post-Error Slowing ($PES$).

---

### 1.3 Working Memory Updating & Context Maintenance
- **Theoretical Framework**: Active monitoring, coding, and revision of working memory contents, replacing obsolete information with incoming relevant representations (*Miyake et al., 2000*; *Morris & Jones, 1990*). Under the Dual Mechanisms of Cognitive Control (DMC) framework (*Braver, 2012*):
  1. *Proactive Control*: Sustained active maintenance of goal-relevant context (cues) in DLPFC prior to target probe onset, biasing attention.
  2. *Reactive Control*: Transient, late-correction retrieval of context on-demand upon probe conflict.
- **Canonical Paradigms**: $n$-Back (1-, 2-, 3-back), AX-Continuous Performance Test (AX-CPT), Keep-Track Task.
- **Observed Manifest Indicators**: Context discriminability index ($d'_{\text{context}} = Z(H_{AX}) - Z(FA_{BX})$), Proactive Behavioral Index ($PBI = \frac{AY_{\text{err}} - BX_{\text{err}}}{AY_{\text{err}} + BX_{\text{err}}}$), load degradation delta ($\Delta d' = d'_{0\text{-Back}} - d'_{2\text{-Back}}$), Drift Diffusion Model (DDM) drift rate ($v$).

---

## 2. Construct–Indicator Mapping Table

| Latent Construct ($\eta$) | Observable Indicator ($Y$) | Functional Directionality | Manifest Formula / Metric | Primary Non-Target Confounds | Methodological & Analytic Isolations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sustained Attention** | Intra-Individual Variability | Latent deficit increases metric | Ex-Gaussian Exponential Tail ($\tau$); $ICV = \frac{SD_{\text{RT}}}{M_{\text{RT}}}$ | Processing speed slowing; uncorrected slow linear trends across blocks. | Trim anticipations ($<150\,\text{ms}$); fit Ex-Gaussian via Maximum Likelihood; de-trend linear time effects before calculating $ICV$. |
| **Sustained Attention** | Omission Error Rate (Misses) | Latent deficit increases metric | $P(\text{Miss}) = \frac{N_{\text{Omission}}}{N_{\text{Target Trials}}}$ | Motor impairment; sensory threshold failure; fast anticipatory responses causing aborts. | Differentiate timed-out misses ($RT > RT_{\text{max}}$) from motor non-execution; evaluate visual acuity checks at baseline. |
| **Sustained Attention** | Vigilance Decrement Slope | Latent deficit steepens slope | $\beta_{\text{Block}} \left(d' \text{ or } M_{\text{RT}}\right) \sim \text{Block Index}$ | Physical/muscular fatigue; loss of motivation / task disengagement. | Rest breaks between paradigms; survival/hazard modeling of lapse probability over continuous trials. |
| **Inhibitory Control** | Commission Error Rate (No-Go / Distractor) | Latent deficit increases metric | $FAR = \frac{N_{\text{False Alarm}}}{N_{\text{Withhold Trials}}}$ | Speed-Accuracy Trade-off (SATO); low prepotency induction (Go rate too low). | Enforce high Go:No-Go ratio ($\ge 75:25$); model boundary separation ($a$) via Drift Diffusion Model to detect SATO. |
| **Inhibitory Control** | Stop-Signal Reaction Time (SSRT) | Latent deficit increases metric | $SSRT = \text{Percentile}(RT_{\text{Go}}, P(\text{Respond}|\text{SSD})) - SSD$ | Strategic Go-trial slowing; violation of race model context independence. | Use dynamic tracking staircase for SSD; implement integration method with replacement of omission errors (*Verbruggen et al., 2019*). |
| **Inhibitory Control** | Post-Error Slowing (PES) | Latent efficiency increases metric | $\overline{RT}_{t+1|\text{Error}} - \overline{RT}_{t+1|\text{Correct}}$ | Post-error orienting reflex / distraction slowing (not true strategic adjustment). | Analyze post-error accuracy; use robust matching estimators avoiding regression to the mean. |
| **WM Updating / Context** | Cue-Driven Discriminability | Latent efficiency increases metric | $d'_{\text{context}} = Z(H_{AX}) - Z(FA_{BX})$ | Sensorimotor processing speed; generalized perceptual discrimination failure. | Contrast $d'_{\text{context}}$ against simple target-detection $d'$; hold stimulus contrast and display dynamics identical. |
| **WM Updating / Context** | Proactive Behavioral Index (PBI) | Latent proactive shift increases metric | $PBI = \frac{AY_{err} - BX_{err}}{AY_{err} + BX_{err}}$ | Low task comprehension; raw omission rate; severe motor impulsivity. | Compute log-linear correction for zero error counts; verify basic task rule mastery during dedicated practice blocks. |
| **WM Updating / Context** | Memory Load Accuracy Drop | Latent deficit increases metric | $\Delta d' = d'_{\text{Baseline}} - d'_{\text{Load}}$ | Perceptual encoding bottleneck; lack of digit familiarity. | Use identical stimulus tokens between baseline and load conditions; measure baseline simple RT. |

---

## 3. Measurement Model Specification

### 3.1 Mathematical Framing
Reflective linear latent variable formulation:
$$Y_{ij} = \nu_j + \lambda_j \eta_i + \gamma_j \mathbf{C}_i + \varepsilon_{ij}$$

Augmented by computational parameter recovery:
1. **Ex-Gaussian Latency Convolutions**:
   $$f(t; \mu, \sigma, \tau) = \frac{1}{\tau\sqrt{2\pi}} \exp\left(\frac{\mu - t}{\tau} + \frac{\sigma^2}{2\tau^2}\right) \Phi\left(\frac{t - \mu}{\sigma} - \frac{\sigma}{\tau}\right)$$
   - $\mu, \sigma$: Sensorimotor execution central tendency and variance.
   - $\tau$: Exponential scale parameter capturing catastrophic attentional lapses.
2. **Wiener First-Passage Time (DDM)**:
   $$dX_t = v\,dt + s\,dW_t$$
   - $v$ (drift rate): Information accumulation rate (context fidelity).
   - $a$ (boundary separation): Strategic response caution (SATO isolation).
   - $t_0$ (non-decision time): Peripheral sensorimotor latency.

---

## 4. Primary Deliverables

### Deliverable 1A: Construct Definition Matrix

```
===================================================================================================================
                                         CONSTRUCT DEFINITION MATRIX
===================================================================================================================
Construct Name: SUSTAINED ATTENTION
  Theoretical Framework: Tonic Alertness & Vigilance Resource Depletion / Default Mode Intrusion
  Anatomical Anchors:   Right Frontoparietal Attentional Network; Locus Coeruleus Noradrenergic System
  Target Latent Factor: Endogenous capacity to maintain attentional engagement across un-cued temporal intervals.
  
  Observed Indicators:
    - Ex-Gaussian Exponential Tail (tau)              [Primary Index; expected range: 50-250 ms]
    - Intra-individual Coefficient of Variation (ICV)  [Secondary Index; ICV = SD_RT / Mean_RT]
    - Omission Rate on High-Prepotency Targets         [Catastrophic Lapse Index; rate < 5% in normal baseline]
    - Temporal Degradation Slope (Block 1 to N)        [Slope beta of RT and d' over session time]
    
  Operational Validation Criteria:
    - Metric must demonstrate significant monotonic deterioration across >= 12 minutes continuous testing.
    - tau must correlate with target omission rate (r >= .40) while showing divergent validity from mu (r <= .20).

-------------------------------------------------------------------------------------------------------------------
Construct Name: SELECTIVE & INHIBITORY CONTROL
  Theoretical Framework: Executive Functions (Miyake 2000); Independent Race Model (Logan & Cowan 1984)
  Anatomical Anchors:   Right Inferior Frontal Cortex (rIFC), Pre-SMA, Subthalamic Nucleus (STN)
  Target Latent Factor: Active suppression of automated, prepotent motor executions upon conflict detection.
  
  Observed Indicators:
    - Commission Error Rate on Withhold Trials         [False Alarm Rate; target prepotency >= 75%]
    - Stop-Signal Reaction Time (SSRT)                 [Non-observable stop latency via integration method]
    - Post-Error Slowing (PES) Delta                   [RT(t+1 | error) - RT(t+1 | correct)]
    - DDM Boundary Separation Parameter (a)            [Inverse metric of impulsivity / threshold caution]
    
  Operational Validation Criteria:
    - Withhold accuracy must vary inversely with target prepotency (Go-probability).
    - SSRT calculation must satisfy the race model independence assumption (Mean RT_uninhibited < Mean RT_Go).

-------------------------------------------------------------------------------------------------------------------
Construct Name: WORKING MEMORY UPDATING & CONTEXT MAINTENANCE
  Theoretical Framework: Dual Mechanisms of Cognitive Control (Braver 2012); Concentric WM Model (Oberauer)
  Anatomical Anchors:   Dorsolateral Prefrontal Cortex (DLPFC), Inferior Parietal Sulcus, Striatum (gating)
  Target Latent Factor: Active goal representation, updating, and maintenance across delay to bias response selection.
  
  Observed Indicators:
    - Context Discriminability Index (d'_context)      [Z(Hit_AX) - Z(FA_BX)]
    - Proactive Behavioral Index (PBI)                 [(AY_err - BX_err) / (AY_err + BX_err)]
    - n-Back Load Degradation Metric (Delta d')        [d'(0-Back) - d'(2-Back)]
    - DDM Drift Rate on Context-Dependent Probes (v)   [Information accumulation speed per condition]
    
  Operational Validation Criteria:
    - Experimental conditions increasing cue-probe delay must selectively impair BX performance under low proactive control.
    - Working memory load must selectively suppress drift rate (v) while preserving non-decision time (t_0).
===================================================================================================================
```

---

### Deliverable 1B: Validity-Risk Register

| Risk ID | Category | Specific Confound / Mechanism | Manifest Impact on Measurement | Methodological Design Mitigation | Analytic / Pipeline Mitigation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **VR-01** | Construct Validity | **Motor Speed Confound:** Peripheral motor velocity variance. | Simple motor slowing inflates mean RT, mistakenly interpreted as WM decay or lapse. | Dedicated Simple Reaction Time (SRT) calibration baseline block. | Decompose RT vectors via DDM; isolate non-decision time ($t_0$) from drift ($v$). |
| **VR-02** | Internal Validity | **Speed-Accuracy Trade-off (SATO):** Strategic shifts favoring speed over precision. | Low commission rate falsely interpreted as high inhibition, when participant elevated caution. | Standardized speed/accuracy instructions; explicit training feedback incentives. | Extract boundary parameter ($a$) via DDM. Reject conclusions based on raw accuracy without RT matching. |
| **VR-03** | Construct Validity | **Proactive vs Reactive Conflation:** Cue neglect vs probe execution failure. | Treating AX-CPT error rates as generic "inattention" rather than gating failure. | Asymmetric probe combinations ($AX, AY, BX, BY$) with 70% $AX$ prepotency baseline. | Compute $PBI$ and $d'_{\text{context}}$ to separate cue-maintenance from target-inhibition. |
| **VR-04** | Statistical Validity | **Non-Normal RT Distributions:** Fitting Gaussian models ($\bar{X}, s$) to skewed RTs. | Inflation of Type I/II errors; misestimation of sustained attention variance. | Minimum 100 trials per functional condition cell for stable tail estimation. | Fit three-parameter Ex-Gaussian distribution ($\mu, \sigma, \tau$) via MLE; log-transform RT for parametric tests. |
| **VR-05** | Statistical Validity | **SDT Boundary Problem:** 0% or 100% Hit or False Alarm rates yielding infinite $Z$-scores. | Undefined $d'$ and extreme variance distortion in high-performing cohorts. | Calibrate task difficulty via psychophysical pilot to avoid ceiling performance ($d' > 4.0$). | Implement standard log-linear correction (*Hautus, 1995*): add 0.5 to cells and 1.0 to trial counts. |
| **VR-06** | Operational Validity | **Visual / Cognitive Fatigue:** Energetic vigilance depletion vs deliberate disengagement. | Gradual performance degradation falsely classified as specific cognitive pathology. | Session constrained to $\le 35\,\text{minutes}$; insert fixed, structured rest intervals between blocks. | Model trial-by-trial hazard rates; compare linear vs step-function temporal decay models in pipeline. |
| **VR-07** | Internal Validity | **Premature Anticipations:** Responses before visual decoding ($RT < 150\,\text{ms}$). | Distortion of RT distributions; falsely elevated commission error rates. | Introduce jittered Inter-Stimulus Intervals (ISI: 1000–1400 ms) to break motor rhythm. | Automated pipeline cleaning: flag and segregate all $RT < 150\,\text{ms}$ into an anticipation error registry. |
| **VR-08** | Construct Validity | **Strategy Drift:** Participant adopts heuristic rules (e.g., ignoring cues, responding to probes). | Invalidation of targeted executive cognitive control architecture. | Explicit feedback during pre-experimental practice blocks; monitor comprehension. | Implement run-length consistency metrics; compute split-half PBI stability across halves. |