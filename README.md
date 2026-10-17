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

## Synthetic Benchmark Validation

To validate the psychometric pipelines prior to empirical data collection, a hierarchical Monte Carlo simulator was used to generate a 20,000-trial synthetic benchmark. The diagnostic plots below confirm that the generated data accurately reproduces target cognitive phenomena:

![Benchmark Validation Diagnostics](data/raw/benchmark_validation_diagnostics.png)

*   **Top-Left:** Conflict Slowing (AY responses are slower than AX responses).
*   **Top-Right:** Latent Tau Recovery (Strong correlation between true and observed attentional lapses).
*   **Bottom-Left:** Working Memory Decay (BX errors increase significantly under long delays).
*   **Bottom-Right:** Time-on-Task Vigilance Drift (Reaction times slow down across the 4 blocks).

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
│   ├── raw/                          # Raw session dumps, benchmark data & diagnostic plots
│   └── processed/                    # Cleaned Parquet tables & subject summary CSVs
├── docs/                             # Complete project documentation suite (Days 1–30)
├── paradigms/
│   ├── psychopy/                     # Deliverable D2: PsychoPy Coder implementation
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
├── synthetic_data/                   # Deliverable D5: Monte Carlo benchmark generator
│   ├── generator.py                  # Hierarchical Ex-Gaussian / SDT generator
│   └── generate_benchmark.py         # Batch production engine (N=50 x 400 trials)
├── analysis_python/                  # Deliverable D6: Python psychometric pipeline
│   ├── ingest.py                     # Ingestion integrity & compliance auditing
│   ├── clean.py                      # Non-destructive MAD outlier filtering
│   ├── sdt.py                        # Hautus (1995) log-linear SDT scoring
│   ├── summarize.py                  # 24-column subject-level aggregator
│   └── cpt_pipeline.py               # Master CLI pipeline orchestrator
├── analysis_r/                       # Deliverable D7: R Tidyverse psychometric pipeline
│   ├── .Rprofile                     # renv local environment hook
│   ├── renv.lock                     # Dependency lockfile template
│   ├── cpt_cleaning_pipeline.R       # Parity-verified tidyverse pipeline
│   └── qa_report.qmd                 # Quarto automated statistical assertion report
├── tests/                            # Test suites & benchmarking harnesses
│   ├── test_config.py                # Configuration bounds & schema tests
│   ├── test_trial_generator.py       # Run-rules & cell distribution tests
│   ├── test_logger_schema.py         # 22-column schema contract tests
│   ├── test_pipeline.py              # MAD filtering & non-destructive tests
│   ├── test_sdt.py                   # Hand-computed Hautus SDT analytical cases
│   ├── verify_timing.py              # Deliverable D4 Part 1: Hardware timing QA
│   ├── plot_diagnostics.py           # Benchmark visualization suite
│   └── verify_equivalence.py         # Cross-language numerical parity audit
├── .gitignore
├── pytest.ini                        # Pytest configuration
├── requirements.txt                  # Pinned Python dependencies
└── requirements-ci.txt               # Dependencies specifically for GitHub Actions
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
Ensure all 25 unit tests pass:
```bash
python -m pytest tests/ -v
```

### 5. Run the R Pipeline (Deliverable D7)
Because R environments vary by system, we provide two supported installation routes:

**Option A: Standard `renv` (Recommended if Rtools is installed)**
```r
# Launch R in the project root:
install.packages("renv")
renv::restore()
source("analysis_r/cpt_cleaning_pipeline.R")
```

**Option B: Conda Fallback (Recommended for Windows/Anaconda users)**
If `renv` fails to compile packages like `arrow`, install the pre-compiled binaries via Conda:
```bash
conda install -c conda-forge --override-channels r-base r-arrow r-dplyr r-purrr r-readr r-tibble r-stringr r-yaml r-quarto -y
```
Then execute the script via the terminal:
```bash
Rscript analysis_r/cpt_cleaning_pipeline.R
```

### 6. Verify Cross-Language Equivalence
Run the automated parity audit to compare the Python and R outputs:
```bash
python tests/verify_equivalence.py
```
*(Note: The test verifies 31 shared psychometric columns. The Python pipeline additionally outputs 5 hardware-level telemetry audit flags that are native to the PsychoPy engine and not generated by the R statistical pipeline).*

---

## Known Limitations (Accepted for v1.0)

The following issues are documented limitations of the current synthetic-benchmark release. They do not impact the core mathematical validity of the pipelines but will be addressed prior to empirical human data collection:

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