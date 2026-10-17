# CDSS Architecture and Contracts (Deliverable D9)

## 1. Purpose

This document defines the Cognitive Decision Support System architecture for the AX-CPT psychometric pipeline.

The CDSS is designed to support human researchers and operators by transforming validated behavioral data into interpretable psychometric evidence, uncertainty estimates, and candidate cognitive concerns.

It is not an autonomous diagnostic system.

## 2. Non-Diagnostic Mandate

This system must not be used for:

- clinical diagnosis
- psychiatric classification
- autonomous medical decision-making
- fitness-for-duty determination
- employment screening
- ADHD, schizophrenia, TBI, or MCI diagnosis

Allowed use:

- research instrumentation
- human factors analysis
- psychometric pipeline validation
- cognitive ergonomics modeling
- human-in-the-loop decision support

## 3. High-Level Architecture

The architecture is organized into four tiers:

    graph TD
      A[Raw Trial Logs] --> B[Ingestion and Schema Validation]
      B -->|Reject Malformed| C[Dead Letter Queue]
      B -->|Valid Data| D[Clean and Audit Pipeline]

      subgraph FEATURE_STORE
        D --> E[Trial Parquet Store]
        D --> F[Psychometric Feature Mart]
        F --> G[Hautus SDT Engine]
        F --> H[Ex-Gaussian and DDM Estimator]
      end

      subgraph INFERENCE
        G --> I[Hierarchical Bayesian Model]
        H --> I
        I --> J[MCMC or Variational Sampler]
        J --> K[Uncertainty Estimator]
        K --> L[95 Percent Credible Intervals]
        K --> M[Normative Deviation Scores]
      end

      subgraph HUMAN_LAYER
        L --> N[Human-in-the-Loop Dashboard]
        M --> N
        N --> O[Analyst Review]
        O --> P[Audit Log and Reproducibility Bundle]
      end

## 4. Tier 1: Ingestion and Schema Validation

Responsibilities:

- read raw CSV or Parquet session files
- validate Raw Data Schema v1.0
- detect duplicate rows
- detect missing trials
- detect malformed response codes
- preserve original row identity
- emit subject validation records

Primary module:

- analysis_python/ingest.py

Required raw fields include:

- participant_id
- trial_index
- trial_type
- cue_stimulus
- probe_stimulus
- required_key
- response_key
- rt_ms
- outcome_code
- block_condition
- cpi_nominal_ms
- timestamp
- frame_drop_detected

## 5. Tier 2: Cleaning and Feature Store

Responsibilities:

- apply non-destructive outlier flagging
- compute within-subject MAD bounds
- preserve rejected or flagged rows
- generate subject-level feature vectors
- store cleaned trial tables
- maintain provenance hashes

Primary modules:

- analysis_python/clean.py
- analysis_python/summarize.py

Cleaning principle:

- Never silently delete data.
- Flag anomalies.
- Record rejection reason.
- Preserve auditability.

Feature contract examples:

| Feature | Type | Unit | Description |
|---|---|---|---|
| ax_omission_rate | float | proportion | AX misses divided by AX trials |
| bx_commission_rate | float | proportion | BX false alarms divided by BX trials |
| ay_error_rate_long_delay | float | proportion | AY errors under long delay |
| d_prime | float | index | SDT sensitivity |
| criterion_c | float | index | SDT response bias |
| conflict_cost_ms | float | milliseconds | BX-related slowing |
| wm_decay_cost_pct | float | percent | Long-delay degradation |
| vigilance_slope_ms | float | ms per trial index | Temporal slowing |
| anticipation_rate | float | proportion | Responses below RT floor |
| frame_drop_count | integer | count | Timing integrity signal |

## 6. Tier 3: Bayesian Inference Engine

Responsibilities:

- estimate subject-level posterior distributions
- propagate measurement uncertainty
- compare observed features to normative or benchmark priors
- produce credible intervals
- avoid deterministic labels without uncertainty

Allowed outputs:

- posterior mean
- posterior HDI
- deviation score
- uncertainty class
- evidence summary

Disallowed outputs:

- binary diagnosis
- autonomous risk label without human review
- clinical category assignment

## 7. Tier 4: Human-in-the-Loop Dashboard

The dashboard must present:

- candidate concern
- supporting metrics
- alternative explanations
- data-quality warnings
- uncertainty interval
- recommended human action
- link to raw provenance

Example output structure:

    candidate_concern: sustained_attention_instability
    evidence:
      ax_omission_rate: 0.18
      threshold: 0.15
      credible_interval: [0.12, 0.24]
    alternative_explanations:
      - duplicate rows detected
      - missing trials detected
      - possible motor disengagement
    data_quality_warnings:
      - ingestion_validation_status: REVIEW_REQUIRED
    recommended_action:
      - inspect raw session logs
      - rerun ingestion validation
      - do not interpret cognitive signal until data quality is resolved

## 8. Alert Classification

Alerts must be separated by class:

1. Data integrity warning
2. Measurement instability warning
3. Candidate cognitive concern
4. Informational note
5. No actionable signal

This prevents alert fatigue and avoids confusing artifacts with cognitive effects.

## 9. Ethical Guardrails

Required guardrails:

- research-use labeling
- no autonomous diagnosis
- uncertainty always displayed
- human override required
- consent and privacy by design
- raw data excluded from public version control
- audit log retained
- limitations visible in every report

## 10. Interfaces

Python pipeline:

    python analysis_python/cpt_pipeline.py --config config/pipeline_config.yaml

R pipeline:

    Rscript analysis_r/cpt_cleaning_pipeline.R

Equivalence audit:

    python tests/verify_equivalence.py

## 11. Evaluation Plan

Evaluation layers:

1. Schema conformance
2. Unit tests
3. Cross-language equivalence
4. Synthetic parameter recovery
5. Injected anomaly detection
6. Human interpretability review
7. Future empirical validation

## 12. Exit Checklist

- Four-tier architecture defined.
- Component contracts specified.
- Data quality separated from cognitive inference.
- Uncertainty display required.
- Human override required.
- Non-diagnostic boundary stated.
- Repository privacy rules enforced.
