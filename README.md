# Behavioral Paradigm Design & Psychometric Pipeline Preparation
### Dual-Delay AX-CPT Research Platform (Deliverables D1–D10)

> **Status:** RESEARCH-USE PROTOTYPE — Synthetic validation complete; cross-language parity verified on shared psychometric columns; empirical pilot pending.
>
> **Quality Assurance:** 25/25 Pytest Unit Tests Passed | Cross-Language Equivalence Verified
>
> **Development Timeline:** 12 months (Iterative design, PSD freeze, polyglot pipeline implementation, and synthetic validation).

---

## Abstract

This repository provides an open-source, reproducible psychophysical experimental paradigm and computational psychometric processing pipeline designed to dissociate three core latent executive functions: **Sustained Attention (Tonic Vigilance)**, **Inhibitory Control (Motor Response Suppression)**, and **Working Memory Context Maintenance**.

Developed as an independent methodological research portfolio, the platform implements a standardized Dual-Delay AX-Continuous Performance Test (AX-CPT) across both PsychoPy Coder (Python 3.11) and OpenSesame 4.x. It is backed by a hierarchical Monte Carlo synthetic data generator and twin analytical pipelines in Python and R.

**This software is strictly an investigational research instrument and does not provide automated clinical diagnosis, psychiatric classification, or autonomous medical decision-making.**

---

## Motivation & Clinical/Educational Context

This project stems from nearly a decade of applied experience in educational consulting and behavioral intervention (specifically within school environments and with families of children on the autism spectrum). In these settings, breakdowns in goal-maintenance, attention regulation, and behavioral inhibition frequently manifest as academic and emotional challenges.

However, relying purely on subjective rating scales limits quantitative assessment. This repository was developed over a 12-month period to bridge that gap: providing a high-precision, sub-millisecond computational framework (Dual-Delay AX-CPT) to objectively decompose proactive versus reactive cognitive control. **Note:** This is a research-use assessment pipeline, not a standalone clinical diagnostic device.

---

## 📁 Repository Structure

```text
📁 cpt-project
├── 📁 analysis_python
│   ├── 🐍 __init__.py
│   ├── 🐍 clean.py
│   ├── 🐍 cpt_pipeline.py
│   ├── 🐍 ingest.py
│   ├── 🐍 sdt.py
│   └── 🐍 summarize.py
├── 📁 analysis_r
│   ├── 📈 cpt_cleaning_pipeline.R
│   ├── 📓 qa_report.qmd
│   └── 📦 renv.lock
├── 📁 config
│   ├── ⚙️ config.yaml
│   ├── ⚙️ pipeline_config.yaml
│   └── 🧾 schema_raw_v1.json
├── 📁 data
│   ├── 📁 processed
│   └── 📁 raw
├── 📁 docs
│   ├── 📁 assets
│   │   ├── 🖼️ benchmark_validation_diagnostics.png
│   │   └── 🖼️ verification_stack.svg
│   ├── 📝 01_construct_definition_matrix.md
│   ├── 📝 02_literature_synthesis_matrix_a.md
│   ├── 📝 03_experimental_design.md
│   ├── 📝 04_timing_state_machine_schema.md
│   ├── 📝 05_psd_v1_frozen.md
│   ├── 📝 06_repo_scaffolding_and_config.md
│   ├── 📝 07_psychopy_timing_engine_spec.md
│   ├── 📝 08_psd_code_traceability_matrix.md
│   ├── 📝 09_logging_contracts_and_simulated_traces.md
│   ├── 📝 10_timing_qa_protocol.md
│   ├── 📝 11_opensesame_build_and_parity_guide.md
│   ├── 📝 12_pilot_protocol_and_triage_tree.md
│   ├── 📝 13_synthetic_data_model_specification.md
│   ├── 📝 14_single_subject_validation_report.md
│   ├── 📝 15_injected_anomaly_manifest.md
│   ├── 📝 16_synthetic_benchmark_manifest.md
│   ├── 📝 17_generator_validation_and_freeze_report.md
│   ├── 📝 18_benchmark_data_dictionary.md
│   ├── 📝 19_pipeline_architecture_and_contracts.md
│   ├── 📝 20_ingestion_validation_report.md
│   ├── 📝 21_cleaning_and_sdt_spec.md
│   ├── 📝 22_r_pipeline_and_quarto_qa_guide.md
│   ├── 📝 23_cross_language_equivalence_report.md
│   ├── 📝 24_testing_and_ci_specification.md
│   ├── 📝 25_benchmark_analysis_and_reproducibility.md
│   ├── 📝 26_cognitive_ergonomics_matrix_b1.md
│   ├── 📝 27_cdss_architecture_and_contracts.md
│   ├── 📝 28_diagnostic_reasoning_matrix_b2.md
│   ├── 📝 29_final_methodological_report.md
│   └── 📝 30_executive_summary_and_closeout.md
├── 📁 paradigms
│   ├── 📁 opensesame
│   │   ├── 📁 inline_scripts
│   │   │   ├── 🐍 feedback_eval.py
│   │   │   ├── 🐍 init_experiment.py
│   │   │   ├── 🐍 score_trial.py
│   │   │   └── 🐍 trial_init.py
│   │   └── 📝 BUILD_STEPS.md
│   └── 📁 psychopy
│       ├── 🐍 __init__.py
│       ├── 🐍 config_loader.py
│       ├── 🐍 engine.py
│       ├── 🐍 logger.py
│       ├── 🐍 main.py
│       ├── 🐍 trial_executor.py
│       ├── 🐍 trial_logic.py
│       └── 🐍 ui.py
├── 📁 reports
│   └── 🐍 make_combined_svg.py
├── 📁 synthetic_data
│   ├── 🐍 __init__.py
│   ├── 🐍 generate_benchmark.py
│   └── 🐍 generator.py
├── 📁 tests
│   ├── 🐍 __init__.py
│   ├── 🐍 plot_diagnostics.py
│   ├── 🧪 test_config.py
│   ├── 🧪 test_logger_schema.py
│   ├── 🧪 test_pipeline.py
│   ├── 🧪 test_sdt.py
│   ├── 🧪 test_trial_generator.py
│   ├── 🐍 verify_equivalence.py
│   └── 🐍 verify_timing.py
├── 🗂️ PROJECT_STRUCTURE.md
├── 🧪 pytest.ini
├── 📖 README.md
├── 📦 requirements-ci.txt
├── 📦 requirements.txt
└── 🧪 test.py
```

---

## 📖 Component & File Glossary

### 🐍 `analysis_python/` (Deliverable D6: Python Psychometric Pipeline)
*   **`__init__.py`**: Package initialization and public API exports.
*   **`clean.py`**: Non-destructive within-subject Median Absolute Deviation (MAD) outlier filtering.
*   **`cpt_pipeline.py`**: Master CLI orchestrator linking ingestion, cleaning, and summarization.
*   **`ingest.py`**: Raw data ingestion, schema validation, and participant compliance auditing.
*   **`sdt.py`**: Signal Detection Theory scoring utilizing Hautus (1995) log-linear corrections.
*   **`summarize.py`**: Aggregates cleaned trials into the 24-column subject-level summary contract.

### 📈 `analysis_r/` (Deliverable D7: R Tidyverse Psychometric Pipeline)
*   **`cpt_cleaning_pipeline.R`**: Parity-verified `tidyverse` and `arrow` pipeline mirroring the Python logic.
*   **`qa_report.qmd`**: Quarto automated statistical assertion and cohort sanity report.
*   **`renv.lock`**: Strict dependency lockfile ensuring R environment reproducibility.

### ⚙️ `config/` (Single Source of Truth)
*   **`config.yaml`**: Master experimental paradigm configuration (timing, stimuli, run-rules).
*   **`pipeline_config.yaml`**: Psychometric cleaning thresholds, MAD constants, and SDT parameters.
*   **`schema_raw_v1.json`**: JSONSchema draft-07 contract enforcing the 22-column Raw Data Schema.

### 📂 `data/` (Git-Ignored Data Stores)
*   **`processed/`**: Output directory for cleaned Parquet tables and subject summary CSVs.
*   **`raw/`**: Output directory for raw session dumps and synthetic benchmark data.

### 📝 `docs/` (30-Day Methodological Documentation Suite)
*   **`assets/benchmark_validation_diagnostics.png`**: Visual proof of Ex-Gaussian tails and parameter recovery.
*   **`assets/verification_stack.svg`**: Terminal-style verification badge summarizing the 35-test stack.
*   **`01` to `05`**: Construct definitions, literature synthesis, experimental design, timing state-machines, and the frozen PSD v1.0.
*   **`06` to `12`**: Repository scaffolding, PsychoPy/OpenSesame engine specs, logging contracts, QA protocols, and pilot triage trees.
*   **`13` to `18`**: Synthetic data model specs, anomaly manifests, benchmark freeze reports, and data dictionaries.
*   **`19` to `25`**: Pipeline architecture, ingestion validation, cross-language equivalence proofs, CI specs, and reproducibility statements.
*   **`26` to `30`**: Cognitive ergonomics mapping, CDSS Bayesian architecture, diagnostic reasoning matrices, final report, and executive close-out.

### 🧠 `paradigms/` (Experimental Execution Engines)
*   **`opensesame/inline_scripts/*.py`**: Python logic for OpenSesame canvas rendering and FSM scoring.
*   **`opensesame/BUILD_STEPS.md`**: Step-by-step GUI build guide for the OpenSesame `.osexp` file.
*   **`psychopy/__init__.py`**: PsychoPy package initialization.
*   **`psychopy/config_loader.py`**: Pydantic-backed YAML configuration validation.
*   **`psychopy/engine.py`**: V-Sync hardware timing, frame-budget watchdog, and clock management.
*   **`psychopy/logger.py`**: Enforces Raw Data Schema v1.0 and writes atomic CSV/JSON outputs.
*   **`psychopy/main.py`**: Application entrypoint handling CLI args and block sequencing.
*   **`psychopy/trial_executor.py`**: Deterministic trial state machine and keyboard polling.
*   **`psychopy/trial_logic.py`**: Bounded rejection sampling engine enforcing behavioral run-rules.
*   **`psychopy/ui.py`**: Criterion-gated practice blocks and countdown rest interfaces.

### 📊 `reports/`
*   **`make_combined_svg.py`**: Utility script to generate rich-terminal SVG verification badges.

### 🎲 `synthetic_data/` (Deliverable D5: Monte Carlo Generator)
*   **`__init__.py`**: Package initialization.
*   **`generate_benchmark.py`**: Batch production engine generating $N=50$ subjects with cryptographic manifests.
*   **`generator.py`**: Hierarchical Ex-Gaussian latency and SDT threshold decision simulator.

### 🧪 `tests/` (Verification & QA Harnesses)
*   **`__init__.py`**: Test package initialization.
*   **`plot_diagnostics.py`**: Generates empirical density and parameter recovery scatter plots.
*   **`test_config.py`**: Asserts YAML bounds and schema integrity.
*   **`test_logger_schema.py`**: Verifies 22-column schema enforcement and negative RT rejection.
*   **`test_pipeline.py`**: Tests MAD edge-cases (identical values, extreme outliers) and non-destructive flagging.
*   **`test_sdt.py`**: Hand-computed analytical Hautus SDT boundary cases (0% / 100% rates).
*   **`test_trial_generator.py`**: Validates 70/10/10/10 cell balancing and run-rule constraints.
*   **`verify_equivalence.py`**: Cross-language numerical parity audit (Python vs. R) within $10^{-6}$ tolerance.
*   **`verify_timing.py`**: Hardware benchmark for display refresh jitter and keyboard polling latency.

### 📄 Root Files
*   **`PROJECT_STRUCTURE.md`**: High-level architectural map of the repository.
*   **`pytest.ini`**: Pytest configuration and warning filters.
*   **`README.md`**: This master operational documentation file.
*   **`requirements-ci.txt`**: Lightweight dependencies for GitHub Actions CI runners.
*   **`requirements.txt`**: Strictly pinned Python 3.11 production dependencies.
*   **`test.py`**: Master Repository Test Contract (validates directory layout, imports, and end-to-end logic).

---

## Synthetic Benchmark Validation

To validate the psychometric pipelines prior to empirical data collection, a hierarchical Monte Carlo simulator was used to generate a 20,000-trial synthetic benchmark. The diagnostic plot below confirms that the generated data accurately reproduces target cognitive phenomena:

![Benchmark Validation Diagnostics](docs/assets/benchmark_validation_diagnostics.png)

*   **Top-Left:** Conflict Slowing (AY responses are slower than AX responses).
*   **Top-Right:** Latent Tau Recovery (Strong correlation between true and observed attentional lapses).
*   **Bottom-Left:** Working Memory Decay (BX errors increase significantly under long delays).
*   **Bottom-Right:** Time-on-Task Vigilance Drift (Reaction times slow down across the 4 blocks).

---

## 🏆 Verification Stack (35 Tests Passed)

![Verification Stack](docs/assets/verification_stack.svg)

> **Fallback (if the SVG does not render in your environment):**
>
> ```
> $ pytest tests/ -v
> ============================= 25 passed in 2.58s ==============================
>
> $ python test.py
> Test Summary: 10 PASSED, 0 FAILED
>
> TOTAL VERIFICATION: 35 TESTS PASSED | CROSS-LANGUAGE PARITY: EQUIVALENT
> ```

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
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Generate the Synthetic Benchmark (Deliverable D5)
```bash
python synthetic_data/generate_benchmark.py --config config/config.yaml --seed 2026
```

### 3. Run the Python Psychometric Pipeline (Deliverable D6)
```bash
python analysis_python/cpt_pipeline.py --config config/pipeline_config.yaml
```

### 4. Run the Pytest Suite
```bash
python -m pytest tests/ -v
```

### 5. Run the R Pipeline (Deliverable D7)

**Option A: Standard `renv` (Recommended if Rtools is installed)**
```r
install.packages("renv")
renv::restore()
source("analysis_r/cpt_cleaning_pipeline.R")
```

**Option B: Conda Fallback (Recommended for Windows/Anaconda users)**
```bash
conda install -c conda-forge --override-channels r-base r-arrow r-dplyr r-purrr r-readr r-tibble r-stringr r-yaml r-quarto -y
Rscript analysis_r/cpt_cleaning_pipeline.R
```

### 6. Verify Cross-Language Equivalence
```bash
python tests/verify_equivalence.py
```
*(Note: The test verifies 31 shared psychometric columns. The Python pipeline additionally outputs 5 hardware-level telemetry audit flags that are native to the PsychoPy engine and not generated by the R statistical pipeline).*

---

## Known Limitations (Accepted for v1.0)

1. **`synthetic_data/generator.py` Timing Jitter Seeding**: Realized timing noise utilizes unseeded `np.random` calls rather than the thread-local subject RNG, causing minor millisecond jitter discrepancies across batch generation runs.
2. **MAD Degenerate-Case Alignment**: The within-subject MAD filter returns `[150.0, 2000.0]` when a subject has zero valid RT records, whereas the test suite asserts a strict clamping policy on identical arrays.
3. **`analysis_python/ingest.py` Hardcoded Continuity Range**: Trial continuity auditing currently asserts a hardcoded 400-trial limit rather than dynamically querying the configuration file.
4. **Cross-Language Deduplication Tie-Breaking**: Sorting invariants prior to deduplication must be enforced explicitly in `verify_equivalence.py` to guarantee perfect alignment between pandas and R.
5. **`tests/plot_diagnostics.py` Tau Proxy**: Panel 2 visualizes a linear quantile proxy rather than calling a direct Maximum Likelihood Ex-Gaussian solver.

---

## Research-Use Only & Ethical Governance Statement

This software repository is engineered solely for quantitative cognitive systems research, human factors engineering, and psychometric methodology development.

1. **Non-Diagnostic Mandate**: This software **is not a medical device** and has not been cleared or approved by the US FDA, European Medicines Agency, or any international regulatory authority. It must not be utilized for clinical diagnostic evaluation, clinical triage, or medical decision-making regarding ADHD, schizophrenia, traumatic brain injury, or mild cognitive impairment.
2. **No Autonomous Decision-Making**: The architecture strictly prohibits autonomous clinical scoring. All metrics represent descriptive psychometric estimates designed for human-in-the-loop analysis with mandatory display of 95% Bayesian Highest Density Intervals (HDI).
3. **Data Privacy**: Keystroke-level timing logs constitute sensitive behavioral data. All data stores must utilize pseudonymous UUIDs with personal identifiers stored in an isolated identity vault.
```

---