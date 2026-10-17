# Pipeline Architecture & Data Contracts (Day 19)

## 1. Unified Polyglot Pipeline Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   SHARED PIPELINE STAGES                               │
├─────────────┬─────────────┬─────────────┬─────────────────┬─────────────┬──────────────┤
│  1. INGEST  │ 2. VALIDATE │  3. CLEAN   │ 4. FEATURE ENG. │ 5. SUMMARIZE│  6. REPORT   │
├─────────────┼─────────────┼─────────────┼─────────────────┼─────────────┼──────────────┤
│ • Read CSVs │ • Check     │ • Absolute  │ • SDT Indices   │ • Per-Cell  │ • Quarto QA  │
│ • Parse     │   Schema    │   Boundaries│   (Log-Linear)  │   Summaries │ • Equivalence│
│   Metadata  │ • Check Run │ • MAD Filter│ • Context Costs │ • Subject-  │   Audits     │
│ • Enforce   │   Rules     │ • Flag Only │ • Time Slopes   │   Level     │ • Rejection  │
│   Types     │ • Attrition │   (No Drops)│ • Post-Error    │   Master    │   Logs       │
└─────────────┴─────────────┴─────────────┴─────────────────┴─────────────┴──────────────┘
```

### Shared Operational Principles
1. **Config-Driven Single Source of Truth**: `config/pipeline_config.yaml` dictates all cutoffs, adjustments, and attrition thresholds.
2. **Fail-Fast Error Policy**: Schema breaches or illegal types abort pipeline execution with explicit row/column error context.
3. **Non-Destructive Cleaning**: No raw trial rows are deleted. Trials are tagged with explicit audit flags.
4. **Numerical Parity**: Floating-point operations harmonized across Python and R using identical MAD scale constants ($k = 1.4826022185056$), sample variance degrees of freedom ($ddof = 1$), and probit functions.

---

## 2. Processed Data Contracts

### 2.1 Data Contract 1: Cleaned Trial Table (`cleaned_trials.parquet`)
Preserves all 22 columns from `Raw Data Schema v1.0` and appends audit flags:
- `flag_dropped_trial` (`BOOLEAN`): True if trial was dropped in logging stream.
- `flag_duplicate_row` (`BOOLEAN`): True if trial index appeared multiple times.
- `flag_anticipation` (`BOOLEAN`): True if $0.0 < RT < 150.0\,\text{ms}$.
- `flag_timeout_lapse` (`BOOLEAN`): True if $RT > 1000.0\,\text{ms}$ or response omitted.
- `flag_absolute_outlier` (`BOOLEAN`): True if $RT < 150.0\,\text{ms}$ or $RT > 2000.0\,\text{ms}$.
- `flag_mad_outlier` (`BOOLEAN`): True if $|RT - \text{Median}| > 3.0 \times \text{MAD}$ on correct $AX$ trials.
- `is_retained_for_rt` (`BOOLEAN`): True iff `is_correct == True` and no outlier flags raised.
- `is_retained_for_sdt` (`BOOLEAN`): True iff `flag_anticipation == False` and `flag_duplicate_row == False`.

### 2.2 Data Contract 2: Per-Subject Summary Table (`subject_summaries.csv`)
24 standardized psychometric columns per participant:
`participant_id`, `group`, `is_compliant`, `exclusion_reason`, `n_trials_raw`, `n_trials_retained_rt`, `ax_hit_rate`, `ay_commission_rate`, `bx_commission_rate`, `by_commission_rate`, `omission_rate_global`, `anticipation_rate`, `rt_mean_ax_ms`, `rt_sd_ax_ms`, `rt_icv_ax`, `dprime_global`, `criterion_global`, `dprime_context`, `pbi_index`, `conflict_cost_ms`, `wm_decay_cost_pct`, `pes_ms`, `vigilance_slope_ms`, `mad_outlier_count`.