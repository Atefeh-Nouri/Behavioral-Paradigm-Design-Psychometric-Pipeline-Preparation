# Ingestion Validation & Cohort Compliance Report (Day 20)

## 1. Validation Run Results

The ingestion engine processed all 50 synthetic benchmark sessions conforming to `Raw Data Schema v1.0`.

```json
{
  "total_sessions_ingested": 50,
  "total_rows_ingested": 19974,
  "sessions_compliant": 49,
  "sessions_rejected": 1,
  "rejection_manifest": [
    {
      "participant_id": "SUBJ_050",
      "rejection_reason": "EXCESSIVE_AX_OMISSIONS_0.1821",
      "ax_omission_rate": 0.1821,
      "raw_row_count": 398,
      "status": "EXCLUDED_FROM_PSYCHOMETRIC_NORMS"
    }
  ],
  "data_integrity_summary": {
    "total_duplicate_rows_identified": 12,
    "total_dropped_trials_identified": 38,
    "schema_conformance_rate": 1.0
  }
}
```

## 2. Integrity Audit
- **Duplicate Detection**: 12 duplicate logging rows were flagged without row deletion.
- **Trial Continuity**: 38 dropped trials were detected across the cohort.
- **Compliance Gating**: Subject 50 was successfully excluded based on exceeding the 15% $AX$ omission threshold.