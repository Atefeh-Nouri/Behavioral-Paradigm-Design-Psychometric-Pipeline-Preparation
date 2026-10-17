# ==============================================================================
# AX-CPT Psychometric Cleaning and Scoring Pipeline (R Implementation, Deliverable D7)
# Conforms to Data Contracts 1 & 2. Matches Python output within 1e-5 tolerance.
# ==============================================================================

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(purrr)
  library(tibble)
  library(stringr)
  library(yaml)
  library(arrow)
})

# 1. Load Single Source of Truth Configuration
config <- yaml::read_yaml("config/pipeline_config.yaml")

# 2. Hautus (1995) SDT Calculation Function
calculate_hautus_sdt <- function(hits, signal_trials, fa, noise_trials) {
  h_adj <- (hits + config$sdt_parameters$hit_adjustment) /
           (signal_trials + config$sdt_parameters$total_signal_adjustment)
  fa_adj <- (fa + config$sdt_parameters$fa_adjustment) /
            (noise_trials + config$sdt_parameters$total_noise_adjustment)

  z_hit <- stats::qnorm(h_adj)
  z_fa <- stats::qnorm(fa_adj)

  d_prime <- z_hit - z_fa
  criterion_c <- -0.5 * (z_hit + z_fa)

  list(d_prime = d_prime, criterion_c = criterion_c)
}

# 3. Batch Ingest & Audit
raw_files <- list.files(
  path = config$io$raw_data_dir,
  pattern = "SUBJ_.*_raw_trials\\.csv$",
  full.names = TRUE
) %>% sort()

if (length(raw_files) == 0) {
  stop(paste("No participant files found in", config$io$raw_data_dir))
}

ingest_subject <- function(f_path) {
  df <- readr::read_csv(f_path, show_col_types = FALSE)
  df <- df %>%
    mutate(
      flag_duplicate_row = duplicated(trial_index_global),
      flag_dropped_trial = FALSE
    )
  df
}

raw_trials <- purrr::map_dfr(raw_files, ingest_subject)

# 4. Non-Destructive Cleaning & MAD Flagging
min_rt  <- config$cleaning_rules$rt_cutoffs_ms$min
max_rt  <- config$cleaning_rules$rt_cutoffs_ms$max
k_mad   <- config$cleaning_rules$mad_filtering$threshold_k
scale_c <- config$cleaning_rules$mad_filtering$scale_constant

cleaned_trials <- raw_trials %>%
  mutate(
    flag_missing_rt       = is.na(rt_ms),
    flag_anticipation     = !is.na(rt_ms) & (rt_ms < min_rt),
    flag_timeout_lapse    = flag_missing_rt | (!is.na(rt_ms) & rt_ms > 1000.0),
    flag_absolute_outlier = !is.na(rt_ms) & (rt_ms < min_rt | rt_ms > max_rt)
  ) %>%
  group_by(participant_id) %>%
  group_modify(~ {
    subj_df <- .x
    ax_correct <- subj_df %>%
      filter(trial_type == "AX", is_correct == TRUE,
             !flag_anticipation, !flag_duplicate_row)

    if (nrow(ax_correct) > 0) {
      med_rt  <- median(ax_correct$rt_ms, na.rm = TRUE)
      mad_val <- scale_c * median(abs(ax_correct$rt_ms - med_rt), na.rm = TRUE)
      low_b   <- max(min_rt, med_rt - (k_mad * mad_val))
      high_b  <- min(max_rt, med_rt + (k_mad * mad_val))

      subj_df <- subj_df %>%
        mutate(
          flag_mad_outlier = !is.na(rt_ms) & (rt_ms < low_b | rt_ms > high_b)
        )
    } else {
      subj_df <- subj_df %>% mutate(flag_mad_outlier = FALSE)
    }
    subj_df
  }) %>%
  ungroup() %>%
  mutate(
    is_retained_for_rt  = is_correct & !flag_duplicate_row &
                          !flag_absolute_outlier & !flag_mad_outlier,
    is_retained_for_sdt = !flag_duplicate_row & !flag_anticipation
  )

# === PYTHON_COLUMN_ORDER_PARITY ==============================================
# verify_equivalence.py asserts strict column ordering matches Python's
# cleaned_trials.parquet. dplyr's group_modify() promotes the grouping variable
# (participant_id) to position 1; Python's order is (session_id, participant_id,
# ...). Restore the canonical order explicitly before writing.
python_col_order <- c(
  "session_id", "participant_id", "block_index", "block_condition",
  "trial_index_global", "trial_index_block", "trial_type",
  "cue_stimulus", "probe_stimulus", "required_key",
  "cpi_nominal_ms", "cpi_realized_ms", "fixation_realized_ms",
  "probe_onset_timestamp", "response_key", "response_timestamp",
  "rt_ms", "is_correct", "outcome_code", "is_anticipation",
  "post_error_trial", "frame_drop_detected",
  "flag_duplicate_row", "flag_dropped_trial", "flag_missing_rt",
  "flag_anticipation", "flag_timeout_lapse", "flag_absolute_outlier",
  "flag_mad_outlier", "is_retained_for_rt", "is_retained_for_sdt"
)
missing_cols <- setdiff(python_col_order, names(cleaned_trials))
if (length(missing_cols) > 0) {
  stop("Cleaned trials missing expected columns: ",
       paste(missing_cols, collapse = ", "))
}
cleaned_trials <- cleaned_trials %>% select(all_of(python_col_order))
# === END PYTHON_COLUMN_ORDER_PARITY ==========================================

# Write Cleaned Trials (Contract 1)
output_dir_r <- config$io$output_r_dir
dir.create(output_dir_r, showWarnings = FALSE, recursive = TRUE)

# Parquet side-effect — retained for any R-side/external consumer that prefers it.
arrow::write_parquet(cleaned_trials,
                     file.path(output_dir_r, "cleaned_trials.parquet"))

# === CROSS-LANGUAGE PARITY CONTRACT (read by tests/verify_equivalence.py) ===
# The verifier loads *this CSV*, not the parquet above, and expects:
#   - filename:        cleaned_trials_r.csv
#   - encoding:        CSV so that _normalise_na() can unify R's "NA"/"N/A"
#                      string sentinels with Python's NaN.
#   - sort key:        (participant_id, trial_index_global) is stable.
# readr::write_csv() writes NA as the literal string "NA" by default, which is
# exactly the sentinel _normalise_na() is designed to collapse.
readr::write_csv(cleaned_trials,
                 file.path(output_dir_r, "cleaned_trials_r.csv"))
# === END CROSS-LANGUAGE PARITY CONTRACT =====================================

# 5. Subject Summary Generation (Contract 2)
summarize_subject <- function(subj_df) {
  subj_id  <- subj_df$participant_id[1]
  subj_nr  <- as.integer(stringr::str_extract(subj_id, "\\d+"))
  group_val <- if (subj_nr %% 2 == 1) "A" else "B"

  total_raw <- nrow(subj_df)

  # --- OUTPUT columns: use is_retained_for_sdt (matches Python summarizer) ---
  ax_trials <- subj_df %>% filter(is_retained_for_sdt, trial_type == "AX")
  ay_trials <- subj_df %>% filter(is_retained_for_sdt, trial_type == "AY")
  bx_trials <- subj_df %>% filter(is_retained_for_sdt, trial_type == "BX")
  by_trials <- subj_df %>% filter(is_retained_for_sdt, trial_type == "BY")

  ax_hits     <- sum(ax_trials$outcome_code == "HIT")
  ax_total    <- nrow(ax_trials)
  ax_hit_rate <- if (ax_total > 0) ax_hits / ax_total else 0.0

  ay_comm <- sum(ay_trials$outcome_code == "COMMISSION_ERROR")
  ay_rate <- if (nrow(ay_trials) > 0) ay_comm / nrow(ay_trials) else 0.0

  bx_comm <- sum(bx_trials$outcome_code == "COMMISSION_ERROR")
  bx_rate <- if (nrow(bx_trials) > 0) bx_comm / nrow(bx_trials) else 0.0

  by_comm <- sum(by_trials$outcome_code == "COMMISSION_ERROR")
  by_rate <- if (nrow(by_trials) > 0) by_comm / nrow(by_trials) else 0.0

  omission_rate      <- sum(subj_df$outcome_code == "OMISSION_ERROR") / total_raw
  anticipation_rate  <- sum(subj_df$flag_anticipation) / total_raw

  # --- COMPLIANCE: replicate Python ingestor exactly -----------------------
  # Python ingestor computes:
  #   ax_trials = df[(df.trial_type == "AX") & (~df.flag_duplicate_row)]
  #   ax_omission_rate = OMISSION_ERROR count / len(ax_trials)
  #   anticipations    = (df.outcome_code == "ANTICIPATION").sum()
  #   anticipation_rate = anticipations / total_rows
  # It does NOT exclude anticipations from the AX denominator and uses the
  # raw outcome_code (not flag_anticipation) for the anticipation count.
  ax_trials_compliance <- subj_df %>%
    filter(trial_type == "AX", !flag_duplicate_row)
  ax_total_compliance <- nrow(ax_trials_compliance)
  ax_omissions_compliance <- sum(
    ax_trials_compliance$outcome_code == "OMISSION_ERROR"
  )
  ax_omiss_rate <- if (ax_total_compliance > 0) {
    ax_omissions_compliance / ax_total_compliance
  } else 1.0

  anticipations_compliance <- sum(subj_df$outcome_code == "ANTICIPATION")
  anticipation_rate_compliance <- if (total_raw > 0) {
    anticipations_compliance / total_raw
  } else 1.0

  is_compliant     <- TRUE
  rejection_reason <- "NONE"

  if (total_raw < config$compliance_thresholds$min_trials_required) {
    is_compliant     <- FALSE
    rejection_reason <- paste0("INSUFFICIENT_TRIALS_COUNT_", total_raw)
  } else if (ax_omiss_rate > config$compliance_thresholds$max_ax_omission_rate) {
    is_compliant     <- FALSE
    rejection_reason <- sprintf("EXCESSIVE_AX_OMISSIONS_%.4f", ax_omiss_rate)
  } else if (anticipation_rate_compliance > config$compliance_thresholds$max_anticipation_rate) {
    is_compliant     <- FALSE
    rejection_reason <- sprintf("EXCESSIVE_ANTICIPATIONS_%.4f",
                                 anticipation_rate_compliance)
  }
  # --- END COMPLIANCE ------------------------------------------------------

  # RT Metrics on Retained AX Trials (ddof=1)
  retained_ax <- subj_df %>% filter(trial_type == "AX", is_retained_for_rt)
  rt_vals <- retained_ax$rt_ms

  if (length(rt_vals) > 1) {
    rt_mean <- mean(rt_vals)
    rt_sd   <- stats::sd(rt_vals)
    rt_icv  <- rt_sd / rt_mean
  } else {
    rt_mean <- 0.0; rt_sd <- 0.0; rt_icv <- 0.0
  }

  # SDT Indices
  all_noise <- nrow(ay_trials) + nrow(bx_trials) + nrow(by_trials)
  all_fa    <- ay_comm + bx_comm + by_comm
  sdt_glob  <- calculate_hautus_sdt(ax_hits, ax_total, all_fa, all_noise)
  sdt_ctx   <- calculate_hautus_sdt(ax_hits, ax_total, bx_comm, nrow(bx_trials))

  # PBI
  pbi <- if ((ay_rate + bx_rate) > 0) {
    (ay_rate - bx_rate) / (ay_rate + bx_rate)
  } else 0.0

  # Contrast Costs
  ay_correct_rt <- subj_df %>%
    filter(trial_type == "AY", outcome_code == "CORRECT_REJECTION",
           is_retained_for_rt) %>%
    pull(rt_ms)
  conflict_cost <- if (length(ay_correct_rt) > 0) {
    mean(ay_correct_rt) - rt_mean
  } else 0.0

  bx_short <- subj_df %>%
    filter(is_retained_for_sdt, trial_type == "BX",
           block_condition == "SHORT_DELAY")
  bx_long <- subj_df %>%
    filter(is_retained_for_sdt, trial_type == "BX",
           block_condition == "LONG_DELAY")
  bx_s_err <- if (nrow(bx_short) > 0) {
    sum(bx_short$outcome_code == "COMMISSION_ERROR") / nrow(bx_short)
  } else 0.0
  bx_l_err <- if (nrow(bx_long) > 0) {
    sum(bx_long$outcome_code == "COMMISSION_ERROR") / nrow(bx_long)
  } else 0.0
  wm_decay_cost <- (bx_l_err - bx_s_err) * 100.0

  # Post-Error Slowing
  post_err_rts  <- retained_ax %>% filter(post_error_trial)  %>% pull(rt_ms)
  post_corr_rts <- retained_ax %>% filter(!post_error_trial) %>% pull(rt_ms)
  pes <- if (length(post_err_rts) > 0 && length(post_corr_rts) > 0) {
    mean(post_err_rts) - mean(post_corr_rts)
  } else 0.0

  # Vigilance Slope
  block_means <- retained_ax %>%
    group_by(block_index) %>%
    summarize(m = mean(rt_ms), .groups = "drop")

  vigilance_slope <- if (nrow(block_means) >= 2) {
    stats::coef(stats::lm(m ~ block_index, data = block_means))[[2]]
  } else 0.0

  tibble::tibble(
    participant_id         = subj_id,
    group                  = group_val,
    is_compliant           = is_compliant,
    exclusion_reason       = rejection_reason,
    n_trials_raw           = total_raw,
    n_trials_retained_rt   = nrow(retained_ax),
    ax_hit_rate            = round(ax_hit_rate, 5),
    ay_commission_rate     = round(ay_rate, 5),
    bx_commission_rate     = round(bx_rate, 5),
    by_commission_rate     = round(by_rate, 5),
    omission_rate_global   = round(omission_rate, 5),
    anticipation_rate      = round(anticipation_rate, 5),
    rt_mean_ax_ms          = round(rt_mean, 5),
    rt_sd_ax_ms            = round(rt_sd, 5),
    rt_icv_ax              = round(rt_icv, 5),
    dprime_global          = round(sdt_glob$d_prime, 5),
    criterion_global       = round(sdt_glob$criterion_c, 5),
    dprime_context         = round(sdt_ctx$d_prime, 5),
    pbi_index              = round(pbi, 5),
    conflict_cost_ms       = round(conflict_cost, 5),
    wm_decay_cost_pct      = round(wm_decay_cost, 5),
    pes_ms                 = round(pes, 5),
    vigilance_slope_ms     = round(vigilance_slope, 5),
    mad_outlier_count      = sum(subj_df$flag_mad_outlier)
  )
}

subject_summaries <- cleaned_trials %>%
  group_split(participant_id) %>%
  purrr::map_dfr(summarize_subject) %>%
  arrange(participant_id)

readr::write_csv(subject_summaries,
                 file.path(output_dir_r, "subject_summaries.csv"))
cat("=== R Pipeline Complete. Outputs saved to", output_dir_r, "===\n")