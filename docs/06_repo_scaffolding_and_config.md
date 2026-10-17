# Repository Architecture & Centralized Configuration (Day 6)

## 1. Directory Structure
The complete directory tree is defined with config, data, docs, paradigms, synthetic_data, analysis_python, analysis_r, and tests folders.

## 2. Configuration Design Principles
Single source of truth resides in config/config.yaml. No magic numbers are allowed in the application code.
