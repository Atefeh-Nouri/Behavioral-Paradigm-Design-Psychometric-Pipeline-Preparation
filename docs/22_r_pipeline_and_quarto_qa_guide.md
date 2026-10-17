# R Tidyverse Pipeline & Quarto Verification Guide (Deliverable D7)

## 1. R Pipeline Architecture (`analysis_r/cpt_cleaning_pipeline.R`)
- Implemented in R 4.4 using `tidyverse` (`dplyr`, `purrr`, `readr`) and `arrow`.
- Ingests raw CSVs, evaluates duplicate flags, applies MAD latency filters, and outputs Data Contract 1 (`cleaned_trials.parquet`) and Data Contract 2 (`subject_summaries.csv`).

## 2. Statistical Parity Constraints
- Enforces MAD scaling constant $k = 1.4826022185056$.
- Enforces sample standard deviation $ddof = 1$ (`stats::sd()`).
- Uses probit link function `stats::qnorm()` matching Python `scipy.stats.norm.ppf()`.

## 3. Quarto Quality Assurance Report (`analysis_r/qa_report.qmd`)
- Automates assertions verifying cohort compliance (exactly 49 compliant, 1 rejected).
- Asserts condition effects: $AY$ conflict slowing $> 40\,\text{ms}$, $BX$ working memory delay degradation $> 10\%$.