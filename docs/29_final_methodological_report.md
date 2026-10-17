# Final Methodological Report (Deliverable D10)

## 1. Abstract

This project designed and implemented a reproducible AX-CPT behavioral paradigm and psychometric pipeline for measuring sustained attention, inhibitory control, and working memory context maintenance.

The deliverables include:

- frozen paradigm specification
- PsychoPy implementation architecture
- OpenSesame parity guidance
- timing QA protocol
- synthetic benchmark generator
- Python psychometric pipeline
- R tidyverse psychometric pipeline
- Signal Detection Theory scoring
- testing and CI specification
- cognitive ergonomics matrix
- CDSS architecture
- diagnostic reasoning literature synthesis
- executive close-out package

The current validation status is synthetic and architectural. Empirical human validation remains future work.

## 2. Construct Rationale

The AX-CPT was selected because it dissociates:

- sustained attention
- inhibitory control
- working memory context maintenance

through controlled cue-probe sequences and delay manipulation.

Primary constructs:

| Construct | Operational Indicator |
|---|---|
| Sustained attention | AX omission rate, vigilance slope |
| Inhibitory control | BX commission rate, conflict cost |
| Working memory context maintenance | AY degradation under LONG_DELAY |
| Response bias | SDT criterion c |
| Sensitivity | SDT d-prime |

## 3. Paradigm Specification Summary

Frozen specification reference:

- docs/05_psd_v1_frozen.md

Key design elements:

- AX-CPT trial taxonomy:
  - AX
  - AY
  - BX
  - BY
- dual-delay structure:
  - SHORT_DELAY
  - LONG_DELAY
- run rules:
  - maximum consecutive targets
  - maximum consecutive non-targets
  - no consecutive identical distractors where configured
- response window logic
- frame-accurate timing requirements
- Raw Data Schema v1.0

## 4. Implementation Architecture

### 4.1 PsychoPy Implementation

Main modules:

- paradigms/psychopy/main.py
- paradigms/psychopy/engine.py
- paradigms/psychopy/trial_logic.py
- paradigms/psychopy/trial_executor.py
- paradigms/psychopy/ui.py
- paradigms/psychopy/logger.py
- paradigms/psychopy/config_loader.py

Design principles:

- no hardcoded experimental parameters
- config-driven execution
- frame-based presentation
- clock management
- dropped-frame logging
- schema-consistent trial logging

### 4.2 OpenSesame Parity

OpenSesame is documented as a parallel implementation target.

References:

- docs/11_opensesame_build_and_parity_guide.md
- paradigms/opensesame/BUILD_STEPS.md

Parity requirements:

- same trial logic
- same timing contracts
- same raw schema
- same response mapping
- same block generation rules

## 5. Synthetic Benchmark

The synthetic benchmark validates pipeline behavior before empirical data collection.

References:

- docs/13_synthetic_data_model_specification.md
- docs/16_synthetic_benchmark_manifest.md
- docs/17_generator_validation_and_freeze_report.md

Benchmark properties:

- multiple subjects
- repeated blocks
- hierarchical between-subject variance
- Ex-Gaussian reaction time structure
- SDT-consistent response generation
- injected anomalies
- ground-truth parameter file
- manifest with checksums

Important limitation:

Synthetic benchmark success demonstrates pipeline behavior under controlled generative assumptions. It does not prove real-world cognitive validity.

## 6. Data Pipeline

### 6.1 Python Pipeline

Modules:

- analysis_python/ingest.py
- analysis_python/clean.py
- analysis_python/sdt.py
- analysis_python/summarize.py
- analysis_python/cpt_pipeline.py

Functions:

- schema validation
- duplicate detection
- missing trial detection
- compliance thresholding
- MAD outlier flagging
- Hautus SDT scoring
- subject summary generation

### 6.2 R Pipeline

Modules:

- analysis_r/cpt_cleaning_pipeline.R
- analysis_r/qa_report.qmd

Functions:

- tidyverse ingestion
- cleaning
- SDT scoring
- subject summaries
- Quarto QA report

## 7. Cross-Language Equivalence

The project requires Python and R pipelines to produce equivalent psychometric results within tolerance.

References:

- docs/23_cross_language_equivalence_report.md
- tests/verify_equivalence.py

Equivalence dimensions:

- row counts
- subject IDs
- compliance flags
- SDT indices
- latency summaries
- error summaries
- outlier counts

## 8. Testing and CI

References:

- docs/24_testing_and_ci_specification.md
- .github/workflows/pipeline_ci.yml

Test layers:

1. config integrity
2. trial generator run-rule satisfaction
3. logger schema validation
4. ingestion validation
5. MAD cleaning
6. SDT boundary conditions
7. cross-language equivalence
8. timing diagnostics

## 9. Results Interpretation Rules

Quantitative result tables must be generated from reproducible pipeline artifacts.

Required output locations:

- data/processed/python/
- data/processed/r/
- reports/
- logs/

Result interpretation must distinguish:

- data-quality failure
- measurement instability
- candidate cognitive concern
- no actionable signal

No result should be reported as clinical evidence.

## 10. Reliability and Validity Discussion

### 10.1 Internal consistency

Future empirical work should assess:

- split-half reliability
- test-retest stability
- internal consistency where appropriate

### 10.2 Construct validity

The design supports construct separation through:

- AX/AY/BX/BY taxonomy
- short/long delay contrast
- SDT sensitivity versus bias decomposition
- non-destructive outlier handling

### 10.3 External validity

Currently limited because:

- data are synthetic
- no participant population has been tested
- no clinical outcome linkage exists

## 11. Limitations

Explicit limitations:

1. Timing precision depends on hardware, OS, display refresh, and PsychoPy configuration.
2. Synthetic data validate pipeline mechanics, not real cognition.
3. CDSS architecture is design-level, not clinically validated.
4. OpenSesame parity requires manual build verification unless automated.
5. R and Python equivalence depends on numerical tolerances and package versions.
6. No empirical calibration of diagnostic thresholds has been performed.

## 12. Future Directions

Potential extensions:

- adaptive Bayesian trial scheduling
- real-time drift monitoring
- physiological multimodal sensing
- empirical validation with controlled participant cohorts
- external replication
- formal human-factors evaluation
- calibrated risk modeling

## 13. Reproducibility Statement

Minimum reproduction workflow:

    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    python synthetic_data/generate_benchmark.py --config config/config.yaml --seed 2026
    python analysis_python/cpt_pipeline.py --config config/pipeline_config.yaml
    Rscript analysis_r/cpt_cleaning_pipeline.R
    pytest tests/ -v
    python tests/verify_equivalence.py

All results must be tied to:

- config hash
- code version
- random seed
- package versions
- input file checksums

## 14. Exit Checklist

- Abstract written.
- Construct rationale documented.
- Paradigm specification summarized.
- Implementation architecture documented.
- Synthetic benchmark role explained.
- Python and R pipelines described.
- Equivalence testing specified.
- Limitations explicitly stated.
- Non-diagnostic governance maintained.
