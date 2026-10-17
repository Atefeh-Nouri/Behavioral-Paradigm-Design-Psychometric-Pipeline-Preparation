# Repository Architecture & Centralized Configuration (Day 6)

## 1. Directory Structure

```text
ax_cpt_cognitive_lab/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   ├── config.yaml               # Master experimental configuration
│   └── pipeline_config.yaml      # Psychometric processing parameters
├── data/
│   ├── raw/                      # Raw participant session dumps (*_raw_trials.csv)
│   └── processed/                # Standardized parquet and summary tables
├── docs/                         # Specification documents and literature matrices
├── paradigms/
│   ├── psychopy/                 # PsychoPy Coder millisecond engine (D2)
│   └── opensesame/               # OpenSesame build hierarchy & inline Python (D3)
├── synthetic_data/               # Monte Carlo benchmark generator (D5)
├── analysis_python/              # Python psychometric pipeline (D6)
├── analysis_r/                   # R tidyverse psychometric pipeline (D7)
└── tests/                        # Verification, benchmark, and unit test suites
```

## 2. Configuration Design Principles
- Single source of truth: `config/config.yaml` controls all runtime display, hardware, timing, stimulus sets, and design blocks.
- No magic numbers: any modification to delays, keybindings, or trial distributions occurs in configuration, not application code.