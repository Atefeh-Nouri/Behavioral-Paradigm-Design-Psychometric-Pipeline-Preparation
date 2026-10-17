# Construct Deconstruction & Measurement Operationalization (Day 1)

## 1. Latent Constructs Deconstruction

### 1.1 Sustained Attention (Vigilance & Tonic Alertness)
- **Theoretical Framework**: Governed by the endogenous capacity to maintain an alert, goal-directed processing state across extended temporal intervals without external prompting (Parasuraman et al., 1998). Supported neuroanatomically by a predominantly right-lateralized frontoparietal network with ascending noradrenergic projections from the locus coeruleus (Aston-Jones & Cohen, 2005).
- **Core Failure Modes**:
  1. Resource Depletion: Processing capacity degrades monotonically as a function of continuous energetic expenditure (Warm, Parasuraman, & Matthews, 2008).
  2. Mind-Wandering / DMN Intrusion: Inability to suppress task-unrelated thoughts (TUTs), leading to periodic sensory attenuation and attentional lapses (Robertson et al., 1997; Weissman et al., 2006).
- **Canonical Paradigms**: Conners CPT, Sustained Attention to Response Task (SART), Psychomotor Vigilance Task (PVT), Mackworth Clock.
- **Observed Manifest Indicators**: Ex-Gaussian exponential tail (τ), intra-individual coefficient of variation (ICV = SD_RT / M_RT), omission error rate (misses), linear RT drift across blocks (β_Block), anticipations (RT < 150 ms).

### 1.2 Selective & Inhibitory Attentional Control
- **Theoretical Framework**: Encompasses processes that suppress prepotent, automatic, or task-irrelevant impulses, mental representations, or behavioral actions (Miyake et al., 2000; Diamond, 2013).
- **Mechanisms**:
  1. Action Cancellation (Response Inhibition): Halting an already initiated motor command, formalized by the Independent Horse-Race Model (Logan & Cowan, 1984). Subserved by right inferior frontal cortex (rIFC), pre-SMA, and the subthalamic nucleus (STN) hyperdirect pathway.
  2. Interference / Conflict Resolution: Resolving competing perceptual/motor representations (Botvinick et al., 2001), governed by anterior cingulate cortex (ACC) and dorsolateral prefrontal cortex (DLPFC).
- **Canonical Paradigms**: Go/No-Go (GNG), Stop-Signal Task (SST), Eriksen Flanker, Stroop.
- **Observed Manifest Indicators**: Commission errors on withhold trials (false alarms), Stop-Signal Reaction Time (SSRT), conflict interference slowing (ΔRT_Conflict), Post-Error Slowing (PES).

### 1.3 Working Memory Updating & Context Maintenance
- **Theoretical Framework**: Active monitoring, coding, and revision of working memory contents, replacing obsolete information with incoming relevant representations (Miyake et al., 2000; Morris & Jones, 1990). Under the Dual Mechanisms of Cognitive Control (DMC) framework (Braver, 2012).
- **Canonical Paradigms**: n-Back (1-, 2-, 3-back), AX-Continuous Performance Test (AX-CPT), Keep-Track Task.
- **Observed Manifest Indicators**: Context discriminability index (d'_context), Proactive Behavioral Index (PBI), load degradation delta (Δd'), Drift Diffusion Model (DDM) drift rate (v).

## 2. Construct–Indicator Mapping Table

| Latent Construct (η) | Observable Indicator (Y) | Functional Directionality | Manifest Formula / Metric | Primary Non-Target Confounds | Methodological & Analytic Isolations |
|----------------------|--------------------------|---------------------------|---------------------------|------------------------------|-------------------------------------|
| Sustained Attention | Intra-Individual Variability | Latent deficit increases metric | Ex-Gaussian Exponential Tail (τ); ICV = SD_RT / M_RT | Processing speed slowing; uncorrected slow linear trends across blocks. | Trim anticipations (<150 ms); fit Ex-Gaussian via Maximum Likelihood; de-trend linear time effects before calculating ICV. |
| Sustained Attention | Omission Error Rate (Misses) | Latent deficit increases metric | P(Miss) = N_Omission / N_Target Trials | Motor impairment; sensory threshold failure; fast anticipatory responses causing aborts. | Differentiate timed-out misses (RT > RT_max) from motor non-execution; evaluate visual acuity checks at baseline. |
| Sustained Attention | Vigilance Decrement Slope | Latent deficit steepens slope | β_Block (d' or M_RT) ~ Block Index | Physical/muscular fatigue; loss of motivation / task disengagement. | Rest breaks between paradigms; survival/hazard modeling of lapse probability over continuous trials. |
| Inhibitory Control | Commission Error Rate (No-Go / Distractor) | Latent deficit increases metric | FAR = N_False Alarm / N_Withhold Trials | Speed-Accuracy Trade-off (SATO); low prepotency induction (Go rate too low). | Enforce high Go:No-Go ratio (≥ 75:25); model boundary separation (a) via Drift Diffusion Model to detect SATO. |
| Inhibitory Control | Stop-Signal Reaction Time (SSRT) | Latent deficit increases metric | SSRT = Percentile(RT_Go, P(Respond|SSD)) - SSD | Strategic Go-trial slowing; violation of race model context independence. | Use dynamic tracking staircase for SSD; implement integration method with replacement of omission errors (Verbruggen et al., 2019). |
| Inhibitory Control | Post-Error Slowing (PES) | Latent efficiency increases metric | RT(t+1|Error) - RT(t+1|Correct) | Post-error orienting reflex / distraction slowing (not true strategic adjustment). | Analyze post-error accuracy; use robust matching estimators avoiding regression to the mean. |
| WM Updating / Context | Cue-Driven Discriminability | Latent efficiency increases metric | d'_context = Z(H_AX) - Z(FA_BX) | Sensorimotor processing speed; generalized perceptual discrimination failure. | Contrast d'_context against simple target-detection d'; hold stimulus contrast and display dynamics identical. |
| WM Updating / Context | Proactive Behavioral Index (PBI) | Latent proactive shift increases metric | PBI = (AY_err - BX_err) / (AY_err + BX_err) | Low task comprehension; raw omission rate; severe motor impulsivity. | Compute log-linear correction for zero error counts; verify basic task rule mastery during dedicated practice blocks. |
| WM Updating / Context | Memory Load Accuracy Drop | Latent deficit increases metric | Δd' = d'_Baseline - d'_Load | Perceptual encoding bottleneck; lack of digit familiarity. | Use identical stimulus tokens between baseline and load conditions; measure baseline simple RT. |

## 3. Measurement Model Specification

### 3.1 Mathematical Framing
Reflective linear latent variable formulation:
Y_ij = ν_j + λ_j η_i + γ_j C_i + ε_ij

Augmented by computational parameter recovery using Ex-Gaussian and Wiener First-Passage Time (DDM) models.
