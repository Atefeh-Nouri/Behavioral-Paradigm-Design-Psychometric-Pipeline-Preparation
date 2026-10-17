# Cognitive Ergonomics & Mental Workload Mapping (Deliverable D8-B1)

## 1. Purpose

This document maps AX-CPT behavioral indices to cognitive ergonomics, mental workload, operator-state monitoring, and human performance constructs.

The goal is not to produce clinical diagnoses. The goal is to define what each observable metric can validly support, what alternative explanations exist, and what extrapolations are invalid.

Primary constructs addressed:

- Sustained attention / vigilance
- Inhibitory control
- Working memory context maintenance
- Response bias
- Error monitoring
- Temporal fatigue / vigilance decrement
- Psychomotor efficiency

## 2. Theoretical Anchors

This matrix is grounded in human factors and cognitive engineering literature, including:

- Wickens' multiple-resource theory
- Parasuraman's automation and human performance work
- Endsley's situation awareness framework
- Signal Detection Theory
- Ex-Gaussian and drift-diffusion models of response latency
- Cognitive failure and vigilance decrement literature

The AX-CPT is treated here as a behavioral measurement instrument, not as a diagnostic device.

## 3. Cognitive Ergonomics Translation Layer

| Behavioral Paradigm Index | Primary Ergonomic / Workload Construct | Theoretical & Mechanistic Anchor | Valid Inference Space | Invalid Extrapolation |
|---|---|---|---|---|
| AX omission rate | Sustained attention failure | Vigilance decrement, locus coeruleus-norepinephrine arousal regulation, mind-wandering | Supports inference of attention lapses or disengagement under task persistence conditions | Cannot by itself diagnose ADHD, fatigue disorder, or clinical inattention |
| BX commission rate | Inhibitory control failure | Right inferior frontal cortex, pre-SMA, basal ganglia gating, response suppression | Supports inference of weakened prepotent response inhibition or impulsive responding | Cannot be interpreted as general impulsivity pathology without broader battery |
| AY error rate under LONG_DELAY | Working memory context maintenance fragility | DLPFC, parietal context maintenance, striatal gating, cue-probe binding | Supports inference of context decay across delay | Cannot isolate working memory capacity without controlling speed-accuracy tradeoff and attention |
| AY short-delay vs long-delay cost | Delay-sensitive context retention | Temporal decay of cue representation | Supports inference of delay-dependent maintenance cost | Cannot prove structural WM deficit without empirical population comparison |
| d-prime | Perceptual/cognitive sensitivity | Signal Detection Theory | Separates response tendency from discriminability | Does not measure intelligence, effort, or clinical severity directly |
| Criterion c | Response bias / strategic setting | SDT decision criterion | Supports inference of liberal vs conservative responding | Cannot be interpreted as motivation or personality without context |
| Mean RT and RT variability | Psychomotor efficiency and stability | Ex-Gaussian distribution, motor execution, arousal | Supports inference of processing speed and response stability | Confounded by hardware, keyboard latency, motor impairment, and practice |
| Vigilance slope | Time-on-task degradation | Fatigue, habituation, arousal decline | Supports inference of temporal performance decline within session | Cannot measure circadian state or chronic fatigue without longitudinal design |
| Post-error slowing | Error monitoring strength | Anterior cingulate cortex, conflict monitoring | Supports inference of behavioral adjustment after errors | Cannot be equated with anxiety, compulsivity, or clinical insight |
| Anticipation rate | Premature responding / impulsivity | Response activation before probe offset | Supports inference of premature response tendency | May also reflect timing misalignment, hardware artifacts, or misunderstanding of task |

## 4. Derived Ergonomic Metrics

The pipeline should compute or preserve the following derived metrics where supported by raw data:

- AX omission rate
- BX commission rate
- AY error rate by delay condition
- d-prime
- Criterion c
- Mean RT by trial type
- Median RT by trial type
- SD RT by trial type
- Ex-Gaussian mu, sigma, tau where estimable
- Conflict cost
- Working memory decay cost
- Post-error slowing
- Vigilance slope
- Anticipation rate
- Frame-drop burden
- Session compliance status

## 5. Signal Detection Theory Integration

Raw accuracy alone is insufficient for ergonomic interpretation.

SDT is required to separate:

- Sensitivity: can the participant distinguish target context from non-target context?
- Bias: does the participant favor responding or withholding responses?

Recommended correction:

- Use Hautus log-linear correction for zero cells.
- Do not use naive proportions when hits, misses, false alarms, or correct rejections are zero.
- Report correction status alongside d-prime and criterion.

## 6. Lab-to-Field Validity Caveats

Extending lab-based AX-CPT indices to real operator settings requires caution.

Major threats:

- Multimodal interference
- Circadian rhythm effects
- Task switching in real environments
- Asymmetric cost functions
- Physical workload
- Environmental distractions
- Motivation differences
- Population differences
- Device latency differences

Therefore, this matrix supports:

- hypothesis generation
- behavioral phenotyping
- human-factors instrumentation
- research-oriented operator-state modeling

It does not support:

- autonomous diagnosis
- fitness-for-duty decisions
- clinical classification
- employment screening without empirical validation

## 7. Traceability

This deliverable must remain traceable to:

- docs/01_construct_definition_matrix.md
- docs/03_experimental_design.md
- docs/04_timing_state_machine_schema.md
- docs/13_synthetic_data_model_specification.md
- docs/21_cleaning_and_sdt_spec.md
- config/config.yaml
- config/pipeline_config.yaml
- analysis_python/sdt.py
- analysis_r/cpt_cleaning_pipeline.R

## 8. Exit Checklist

- Paradigm metrics mapped to ergonomic constructs.
- Valid inference space documented for each metric.
- Invalid extrapolations explicitly blocked.
- SDT integration specified.
- Lab-to-field caveats documented.
- Non-diagnostic governance maintained.
