# Diagnostic Reasoning & CDSS Literature Synthesis (Deliverable D8-B2)

## 1. Synthesis Matrix B2: Diagnostic Reasoning & Cognitive Systems

This synthesis analyzes human diagnostic reasoning, clinical decision-support architectures, cognitive failure modes, and international reporting guidelines (*Croskerry, 2003, 2009*; *Parasuraman & Riley, 1997*; *Lee & See, 2004*; *Vasey et al., 2022* [DECIDE-AI]).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DIAGNOSTIC REASONING FRAMEWORK                            │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│ System 1: Fast, Heuristic, Pattern-Based  │ System 2: Slow, Analytic, Probabilistic    │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ • Vulnerable to Premature Closure         │ • Calibrated via Bayesian Posterior HDIs   │
│ • Vulnerable to Automation Bias / Anchors │ • Forced Evaluation of Counter-Evidence    │
│ • Susceptible to Alert Fatigue & Shuts    │ • Interactive What-If Parameter Auditing   │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

| Domain / Concept | Seminal Theoretical Foundations | Core Mechanism / Phenomenological Failure Mode | Empirical Impact on Clinical Cognition | Design Mitigation Applied in Day 27 Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **Dual-Process Diagnostic Theory** | Croskerry (2003, 2009); Kahneman (2011) | Heuristic, pattern-matching (System 1) vs. slow, deliberative, analytic deduction (System 2). Cognitive shortcuts lead to premature diagnostic closure. | Diagnostic errors in 10–15% of complex cases; clinicians anchor on initial salient laboratory abnormal flags and cease information gathering (*Croskerry, 2003*). | Interface forces System 2 analytical processing: displays full credible interval spreads and suppresses discrete "abnormal/normal" binary diagnostic flags. |
| **Bayesian Probabilistic Updating** | Eddy (1982); Gigerenzer & Hoffrage (1995) | Base-rate neglect and confusion of the inverse ($P(D \mid +) \neq P(+ \mid D)$). Human minds struggle with abstract conditional probabilities. | Clinicians systematically overestimate disease probability by $10\times$ following positive screening tests due to ignoring low population base rates (*Gigerenzer & Hoffrage, 1995*). | Engine operates natively in natural frequencies and Bayesian posterior credible intervals; maps individual features against calibrated normative reference distributions. |
| **Automation Bias & Complacency** | Parasuraman & Riley (1997); Mosier & Skitka (1996) | Humans treat automated system outputs as an authoritative heuristic shortcut, offloading cognitive vigilance to the algorithm. | **Omission errors:** Clinician misses a subtle clinical sign because the CDSS did not flag it. **Commission errors:** Clinician endorses an incorrect CDSS recommendation (*Mosier & Skitka, 1996*). | Architecture prohibits automated classification recommendations; functions strictly as an informational tool displaying raw features alongside Bayesian uncertainty intervals. |
| **Alert Fatigue & Desensitization** | Cash (2009); Phansalkar et al. (2010) | High frequency of false-positive, clinically irrelevant, or unprioritized notifications degrades user responsiveness. | Override rates exceed 90–95% for standard hospital interruptive pop-up alerts, leading clinicians to silence critical warnings (*Phansalkar et al., 2010* [verify]). | Zero interruptive pop-up notifications; non-blocking contextual dashboard embeds findings passively within the clinician's review workflow. |
| **Trust Calibration Dynamics** | Lee & See (2004) | The alignment between a human operator’s subjective trust in an automated tool and the tool’s actual objective capability. | **Overtrust (Misuse):** Uncritical reliance leading to catastrophe. **Undertrust (Disuse):** Premature rejection of valid algorithmic guidance (*Lee & See, 2004*). | Calibrates trust by exposing internal uncertainty: visualizes MCMC convergence metrics ($\hat{R}$), sampling error bounds, and potential confound flags. |
| **CDSS Evaluation Standards** | DECIDE-AI (Vasey et al., 2022); STARD-AI | Guidelines governing early-stage clinical evaluation of artificial intelligence decision-support systems. | Prevents deployment of brittle, non-generalizable black-box algorithms by mandating error analysis, human-factors safety, and user-override audits. | Architecture complies with DECIDE-AI: includes complete data-lineage logging, user-override capture, and non-deterministic Bayesian uncertainty estimation. |

---

## 2. Architectural Gap Analysis: System Design vs. Clinical Literature

1. **What the Literature Validates**:
   - *Passive Alerting*: Concurs with alert fatigue findings (*Phansalkar et al., 2010*), confirming that non-interruptive visual embedding preserves clinical vigilance.
   - *Uncertainty Display*: Validates Croskerry’s debiasing principles by forcing deliberative System 2 processing through 95% Highest Density Interval (HDI) rendering.
2. **Design Hardening Applied**:
   - *Active Counter-Evidence Framing*: Added visual counter-evidence 
displays (e.g., highlighting intact 
A
Y
AY
 performance or preserved motor speed when 
B
X
BX
 errors are elevated) to counteract confirmation bias and premature closure (Nickerson, 1998).
Interactive Sensitivity Audits: Clinicians can toggle demographic and normative reference sets (e.g., age-matched vs. education-matched distributions) to inspect how shifting normative baselines alters the subject's percentile position.
Open Gaps for Future Research:
Longitudinal State Tracking: The architecture currently processes single assessment snapshots. Clinical decision support requires longitudinal state models (e.g., Hidden Markov Models or Dynamic Bayesian Networks) to track disease progression over months or years.
EHR Integration: The current engine operates on isolated behavioral data files. True clinical deployment requires bidirectional HL7 FHIR interfaces to integrate patient records with electronic health records.