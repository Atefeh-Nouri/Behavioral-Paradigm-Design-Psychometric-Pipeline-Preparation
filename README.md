# Behavioral Paradigm Design & Psychometric Pipeline Preparation
### Dual-Delay AX-CPT Research Platform (Deliverables D1–D10)

> **Status: DRAFT — pre-validation**

---

## Abstract
This repository provides an open-source, reproducible psychophysical experimental paradigm and computational psychometric processing pipeline designed to dissociate three core latent executive functions: **Sustained Attention (Tonic Vigilance)**, **Inhibitory Control (Motor Response Suppression)**, and **Working Memory Context Maintenance**. Developed as an independent methodological research portfolio, the platform implements a standardized Dual-Delay AX-Continuous Performance Test (AX-CPT) across both PsychoPy Coder (Python 3.11) and OpenSesame 4.x, backed by a hierarchical Monte Carlo synthetic data generator and twin analytical pipelines in Python and R. **This software is strictly an investigational research instrument and does not provide automated clinical diagnosis, psychiatric classification, or autonomous medical decision-making.**

---

## Repository Structure

```text
ax_cpt_cognitive_lab/
├── .github/
│   └── workflows/
│       └── pipeline_ci.yml           # Automated unit testing & cross-language equivalence CI
├── config/
│   ├── config.yaml                   # Master experimental paradigm configuration (PSD v1.0)
│   ├── pipeline_config.yaml          # Psychometric cleaning & scoring parameters
│   └── schema_raw_v1.json            # JSONSchema draft-07 contract for Raw Data Schema v1.0
├── data/
│   ├── raw/                          # Raw session dumps (*_raw_trials.csv) & benchmark data
│   └── processed/                    # Cleaned Parquet tables & subject summary CSVs
├── docs/                             # Complete project documentation suite (Days 1–30)
│   ├── 01_construct_definition_matrix.md
│   ├── 02_literature_synthesis_matrix_a.md
│   ├── 03_experimental_design.md
│   ├── 04_timing_state_machine_schema.md
│   ├── 05_psd_v1_frozen.md           # Deliverable D1 (FROZEN v1.0)
│   ├── 06_repo_scaffolding_and_config.md
│   ├── 07_psychopy_timing_engine_spec.md
│   ├── 08_psd_code_traceability_matrix.md
│   ├── 09_logging_contracts_and_simulated_traces.md
│   ├── 10_timing_qa_protocol.md      # Deliverable D4 Part 1
│   ├── 11_opensesame_build_and_parity_guide.md
│   ├── 12_pilot_protocol_and_triage_tree.md # Deliverable D4 Part 2
│   ├── 13_synthetic_data_model_specification.md
│   ├── 14_single_subject_validation_report.md
│   ├── 15_injected_anomaly_manifest.md
│   ├── 16_synthetic_benchmark_manifest.md # Deliverable D5 Part 1
│   ├── 17_generator_validation_and_freeze_report.md # Deliverable D5 Part 2
│   ├── 18_benchmark_data_dictionary.md # Deliverable D5 Part 3
│   ├── 19_pipeline_architecture_and_contracts.md
│   ├── 20_ingestion_validation_report.md
│   ├── 21_cleaning_and_sdt_spec.md
│   ├── 22_r_pipeline_and_quarto_qa_guide.md
│   ├── 23_cross_language_equivalence_report.md
│   ├── 24_testing_and_ci_specification.md
│   ├── 25_benchmark_analysis_and_reproducibility.md # Deliverables D6 & D7 Freeze
│   ├── 26_cognitive_ergonomics_matrix_b1.md # Deliverable D8-B1
│   ├── 27_cdss_architecture_and_contracts.md # Deliverable D9
│   ├── 28_diagnostic_reasoning_matrix_b2.md # Deliverable D8-B2
│   ├── 29_final_methodological_report.md # Deliverable D10
│   └── 30_executive_summary_and_closeout.md
├── paradigms/
│   ├── psychopy/                     # Deliverable D2: PsychoPy Coder implementation
│   │   ├── __init__.py
│   │   ├── config_loader.py          # Pydantic configuration validation
│   │   ├── engine.py                 # V-Sync hardware timing & frame-drop watchdog
│   │   ├── trial_logic.py            # Bounded rejection sampling run-rule engine
│   │   ├── trial_executor.py         # Deterministic trial state machine
│   │   ├── ui.py                     # Criterion practice & countdown rest UI
│   │   ├── logger.py                 # Raw Data Schema v1.0 enforcement
│   │   └── main.py                   # Application entrypoint
│   └── opensesame/                   # Deliverable D3: OpenSesame implementation
│       ├── BUILD_STEPS.md            # Step-by-step GUI build guide (<30 min setup)
│       └── inline_scripts/           # Python scripts for OpenSesame items
│           ├── init_experiment.py
│           ├── trial_init.py
│           ├── score_trial.py
│           └── feedback_eval.py
├── synthetic_data/                   # Deliverable D5: Monte Carlo benchmark generator
│   ├── __init__.py
│   ├── generator.py                  # Hierarchical Ex-Gaussian / SDT generator
│   └── generate_benchmark.py         # Batch production engine (N=50 x 400 trials)
├── analysis_python/                  # Deliverable D6: Python psychometric pipeline
│   ├── __init__.py
│   ├── ingest.py                     # Ingestion integrity & compliance auditing
│   ├── clean.py                      # Non-destructive MAD outlier filtering
│   ├── sdt.py                        # Hautus (1995) log-linear SDT scoring
│   ├── summarize.py                  # 24-column subject-level aggregator
│   └── cpt_pipeline.py               # Master CLI pipeline orchestrator
├── analysis_r/                       # Deliverable D7: R Tidyverse psychometric pipeline
│   ├── .Rprofile                     # renv local environment hook
│   ├── renv.lock                     # Dependency lockfile template
│   ├── renv/
│   │   └── activate.R                # renv bootstrap script
│   ├── cpt_cleaning_pipeline.R       # Parity-verified tidyverse pipeline
│   └── qa_report.qmd                 # Quarto automated statistical assertion report
├── tests/                            # Test suites & benchmarking harnesses
│   ├── __init__.py
│   ├── test_config.py                # Configuration bounds & schema tests
│   ├── test_trial_generator.py       # Run-rules & cell distribution tests
│   ├── test_logger_schema.py         # 22-column schema contract tests
│   ├── test_pipeline.py              # MAD filtering & non-destructive tests
│   ├── test_sdt.py                   # Hand-computed Hautus SDT analytical cases
│   ├── verify_timing.py              # Deliverable D4 Part 1: Hardware timing QA
│   ├── plot_diagnostics.py           # Benchmark visualization suite
│   └── verify_equivalence.py         # Cross-language numerical parity audit
├── .gitignore
└── requirements.txt                  # Pinned Python dependencies
```

---

## Quickstart

### 1. Python Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
# source .venv/bin/activate

# Install pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run Synthetic Benchmark Generation (Deliverable D5)
```bash
python synthetic_data/generate_benchmark.py --config config/config.yaml --seed 2026
```

### 3. Run Python Psychometric Processing Pipeline (Deliverable D6)
```bash
python analysis_python/cpt_pipeline.py --config config/pipeline_config.yaml
```

### 4. Run Pytest Suite
```bash
python -m pytest tests/ -v
```

### 5. R Environment Setup & Pipeline Execution (Deliverable D7)
```r
# Launch R in the project root:
install.packages("renv")
renv::restore()

# Execute the R tidyverse cleaning and scoring pipeline:
source("analysis_r/cpt_cleaning_pipeline.R")
```

### 6. Verify Cross-Language Equivalence
```bash
python tests/verify_equivalence.py
```

---

## Known Issues (Pending Local Validation)

Prior to conducting empirical human testing, the following implementation details are slated for hardening during local verification:

1. **`synthetic_data/generator.py` Timing Jitter Seeding**: In `_build_record`, realized timing noise (`cpi_realized_ms` and `fixation_realized_ms`) utilizes unseeded `np.random` calls rather than the thread-local subject RNG (`rng`). This can cause minor millisecond jitter discrepancies across multiple batch generation runs despite a constant master seed.
2. **MAD Degenerate-Case Alignment**: The within-subject MAD filter in `analysis_python/clean.py` returns `[150.0, 2000.0]` when a subject has zero valid RT records, whereas `tests/test_pipeline.py` asserts `high_b == 400.0` on an adversarial all-identical array. The clamping policy must be harmonized.
3. **`analysis_python/ingest.py` Hardcoded Continuity Range**: Trial continuity auditing currently asserts `expected_indices = np.arange(1, 401)` rather than dynamically querying `config["design"]["total_experimental_trials"]`.
4. **Cross-Language Deduplication Tie-Breaking**: `pandas.DataFrame.duplicated(keep="first")` and R's `duplicated()` handle duplicate sequence records identically under natural ordering, but sorting invariants prior to deduplication must be enforced explicitly in `verify_equivalence.py`.
5. **`tests/plot_diagnostics.py` Tau Proxy**: Panel 2 currently visualizes a linear quantile proxy ($Q_{90} - Q_{50}$) rather than calling a direct Maximum Likelihood Ex-Gaussian solver.

---

## Research-Use Only & Ethical Governance Statement

This software repository is engineered solely for quantitative cognitive systems research, human factors engineering, and psychometric methodology development.

1. **Non-Diagnostic Mandate**: This software **is not a medical device** and has not been cleared or approved by the US FDA, European Medicines Agency, or any international regulatory authority. It must not be utilized for clinical diagnostic evaluation, clinical triage, or medical decision-making regarding ADHD, schizophrenia, traumatic brain injury, or mild cognitive impairment.
2. **No Autonomous Decision-Making**: The architecture strictly prohibits autonomous clinical scoring. All metrics represent descriptive psychometric estimates designed for human-in-the-loop analysis with mandatory display of 95% Bayesian Highest Density Intervals (HDI).
3. **Data Privacy**: Keystroke-level timing logs constitute sensitive behavioral data. All data stores must utilize pseudonymous UUIDs with personal identifiers stored in an isolated identity vault.