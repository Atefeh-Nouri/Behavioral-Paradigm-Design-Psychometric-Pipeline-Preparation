# Cognitive Ergonomics & Mental Workload Mapping (Deliverable D8-B1)

## 1. Synthesis Matrix B1: Cognitive Ergonomics Translation Layer

This matrix operationalizes the translation between experimental AX-CPT indices and human factors engineering, neuroergonomics, and operator-state monitoring constructs (*Wickens, 2002, 2008*; *Parasuraman et al., 2000*; *Endsley, 1995*). Every mapping explicitly defines allowable inferences alongside invalid extrapolations.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COGNITIVE ERGONOMICS TRANSLATION LAYER                          │
├──────────────────────────┬────────────────────────────┬────────────────────────────────┤
│ Micro-Behavioral Metric  │ Intermediate State Proxy   │ Macro Ergonomic Construct      │
├──────────────────────────┼────────────────────────────┼────────────────────────────────┤
│ • RT Tail (Tau) / ICV    │ • Attentional Fluctuation  │ • Tonic Vigilance Depletion    │
│ • AY Commission Errors   │ • Impulsive Motor Gating   │ • Action Slip Under High Load  │
│ • BX Errors (Long Delay) │ • Context Representation   │ • Loss of Situation Awareness  │
│ • Target Misses (Omiss)  │ • Perceptual Decoupling    │ • System Boundary Neglect      │
└──────────────────────────┴────────────────────────────┴────────────────────────────────┘
```

| Behavioral Paradigm Index | Primary Ergonomic / Workload Construct | Theoretical & Mechanistic Anchor | Valid Inference Space (What It CAN Support) | Invalid Extrapolation (What It CANNOT Support) |
| :--- | :--- | :--- | :--- | :--- |
| **Intra-Individual RT Variability ($ICV$) & Ex-Gaussian Tail ($\tau$)** | **Tonic Alertness Degradation / Micro-Lapses** | Locus coeruleus noradrenergic dysregulation (*Aston-Jones & Cohen, 2005*); Default Mode Network (DMN) intrusion (*Weissman et al., 2006*). | Indexes an operator’s endogenous ability to suppress task-unrelated thoughts (TUTs) and maintain temporal stability during unpaced, monotonous supervisory monitoring. | Cannot infer chronic pathological sleep disorders, operational burnout, or real-time clinical drowsiness without concurrent physiological telemetry (e.g., EEG theta/beta ratio, PERCLOS eye-tracking). |
| **Conflict Slowing Cost ($\Delta RT_{AY}$) & $AY$ Commissions** | **Executive Action-Slip Vulnerability / Automaticity Capture** | Multiple Resource Theory (*Wickens, 2008*); Rasmussen's Skills-Rules-Knowledge (SRK) framework (Capture slips from Skill-based to Rule-based execution). | Measures vulnerability to routine motor capture when a salient default cue triggers automatic actions that contradict emergent safety conditions. | Cannot predict physical control compliance under high dynamic g-forces, gross motor panic, or novel crisis-management scenarios containing no pre-trained behavioral rules. |
| **Working Memory Delay Decay ($\Delta BX_{\text{Long} - \text{Short}}$)** | **Loss of Situation Awareness (SA Level 2 & 3: Comprehension & Projection)** | Situation Awareness Model (*Endsley, 1995*); Concentric Working Memory Model (*Oberauer, 2002*). | Reflects decay of active context representations over temporal delays; quantifies susceptibility to forgetting transient tactical state changes during unprompted delays. | Cannot determine whether an operator possesses correct long-term procedural domain knowledge (mental model integrity) versus short-term sensory cache decay. |
| **Global Target Omission Rate (Misses)** | **Perceptual Decoupling / Vigilance Collapse** | Sustained Attention Depletion Hypothesis (*Warm et al., 2008*); Perceptual Load Theory (*Lavie, 2005*). | Flags gross operational disengagement, severe sensory decoupling, or channel saturation where primary visual alerts fail to break processing thresholds. | Cannot differentiate physical motor incapacitation (e.g., peripheral limb freezing, hardware switch mechanical disconnect) from pure neurocognitive neglect. |
| **Signal Detection Sensitivity ($d'$) & Bias ($c$)** | **Alarm Trust Calibration & Perceptual Discriminability** | Theory of Signal Detectability (*Green & Swets, 1966*); Automation Trust Calibration (*Lee & See, 2004*). | Separates an operator’s true sensory/informational discrimination capacity ($d'$) from strategic, payoff-driven shifts in conservative vs. liberal reporting thresholds ($c$). | Cannot predict team-level coordinated detection performance or organizational compliance where operator decision thresholds are externally dictated by policy. |
| **Post-Error Slowing ($PES$)** | **Adaptive Error Monitoring & Strategic Regrouping** | Cognitive Control & Conflict Monitoring (*Botvinick et al., 2001*); Post-error orienting reflex (*Notebaert et al., 2009*). | Measures functional cognitive flexibility: whether an operator dynamically raises their response threshold and engages in deliberate verification following an acknowledged error. | Cannot assess emotional resilience, post-traumatic operational freeze, or moral injury resulting from high-consequence operational failures. |

---

## 2. Measurement-Validity Caveats: Lab-to-Operational Boundaries

1. **Synthetic Isolation vs. Multimodal Cross-Talk**: In the laboratory AX-CPT, stimuli appear against a static background. Operational environments require concurrent processing across auditory radio calls, ambient buzzers, visual displays, and tactile controls. High lab $d'$ does not guarantee immunity to cross-modal sensory masking (*Wickens, 2002*).
2. **Temporal Compression vs. Circadian Shift Dynamics**: The 31.2-minute testing window cannot be linearly extrapolated to 8- or 12-hour operational shifts where vigilance interacts with circadian nadirs (e.g., 03:00 to 05:00 AM) without biomathematical sleep-wake modeling (*Hursh et al., 2004* [verify]).
3. **Symmetric Loss Functions vs. Asymmetric Operational Stakes**: Laboratory omissions cost only an unearned score increment. In critical telemetry, an omission represents an unmanaged catastrophe, whereas false alarms cause nuisance alerts. Response criteria ($c$) are shaped by arbitrary laboratory payoffs and are not fixed personality traits.
4. **Physical Restriction vs. Embodied Interaction**: Laboratory chin-rests and keypresses suppress natural motor compensation (posture shifts, pacing, scanning) that operators endogenously recruit to combat fatigue in the field.