# Testing Strategy & Continuous Integration Specification (Day 24)

## 1. Test Suite Architecture (`tests/`)

1. **SDT Mathematical Edge Cases (`test_sdt.py`, `test_pipeline.py`)**:
   - Asserts recovery of $d'$ and $c$ under zero false alarm and zero hit boundaries.
   - Verifies Hautus log-linear probit outputs against analytical hand calculations.
2. **Adversarial MAD Input Handling**:
   - Verifies handling of identical RT values ($\text{MAD} = 0$) without division by zero.
   - Tests resistance to extreme individual lapse outliers.
3. **Data Integrity & Non-Destructive Invariance**:
   - Asserts that flagging operations preserve exact row counts.
4. **Cross-Language Equivalence Harness (`verify_equivalence.py`)**:
   - Compares parquet and CSV tables between Python and R within $1 \times 10^{-5}$ tolerance.

## 2. GitHub Actions CI Pipeline (`.github/workflows/pipeline_ci.yml`)
- Multi-stage pipeline:
  1. `python-test-suite`: Runs pytest and executes Python psychometric pipeline.
  2. `r-pipeline-check`: Executes R tidyverse pipeline within a `rocker/tidyverse:4.4.0` container.
  3. `cross-language-equivalence`: Validates bit-level flag parity and summary numerical tolerance.