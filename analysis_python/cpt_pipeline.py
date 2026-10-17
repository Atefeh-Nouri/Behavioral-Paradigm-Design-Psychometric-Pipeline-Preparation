"""
Master CLI Orchestrator for the Python Psychometric Pipeline (Deliverable D6).
Executes: Ingest -> Validate -> Clean -> Feature Engineer -> Summarize -> Export.
"""

import argparse
from dataclasses import asdict
import json
import os
import sys
import pandas as pd
import yaml

# Cross-module import support
try:
    from analysis_python.ingest import DataIngestor
    from analysis_python.clean import flag_trial_anomalies
    from analysis_python.summarize import summarize_subject_session
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from analysis_python.ingest import DataIngestor
    from analysis_python.clean import flag_trial_anomalies
    from analysis_python.summarize import summarize_subject_session


def run_pipeline(config_path: str = "config/pipeline_config.yaml") -> None:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    out_dir = config["io"]["output_python_dir"]
    os.makedirs(out_dir, exist_ok=True)

    print("=== AX-CPT Python Psychometric Pipeline Execution ===")
    print(f"Reading raw data from: {config['io']['raw_data_dir']}")

    # 1. Ingestion & Validation Stage
    ingestor = DataIngestor(config_path)
    combined_raw_df, validation_records = ingestor.ingest_all_sessions()
    print(f"Ingested {len(validation_records)} subjects ({len(combined_raw_df)} total raw rows).")

    # 2. Non-Destructive Cleaning & Outlier Flagging Stage
    print("Applying non-destructive MAD and latency filtering...")
    cleaned_trials_df = flag_trial_anomalies(combined_raw_df, config)

    # Export Data Contract 1: Cleaned Trials Table (Parquet)
    cleaned_parquet_path = os.path.join(out_dir, "cleaned_trials.parquet")
    cleaned_trials_df.to_parquet(cleaned_parquet_path, index=False)
    print(f"Exported Cleaned Trials (Contract 1): {cleaned_parquet_path}")

    # 3. Psychometric Feature Engineering & Subject Aggregation Stage
    print("Computing SDT and response metrics per participant...")
    val_map = {rec.participant_id: rec for rec in validation_records}
    summary_rows = []

    for subj_id, subj_group in cleaned_trials_df.groupby("participant_id"):
        rec = val_map[subj_id]
        subj_summary = summarize_subject_session(
            subj_group,
            is_compliant=rec.is_compliant,
            rejection_reason=rec.rejection_reason
        )
        summary_rows.append(subj_summary)

    subject_summaries_df = pd.DataFrame(summary_rows).sort_values("participant_id").reset_index(drop=True)

    # Export Data Contract 2: Per-Subject Summary Table (CSV)
    summary_csv_path = os.path.join(out_dir, "subject_summaries.csv")
    subject_summaries_df.to_csv(summary_csv_path, index=False)
    print(f"Exported Subject Summaries (Contract 2): {summary_csv_path}")

    # 4. Export Validation Manifest
    val_manifest = {
        "pipeline_version": config["version"],
        "total_subjects": len(validation_records),
        "compliant_subjects": sum(1 for r in validation_records if r.is_compliant),
        "rejected_subjects": sum(1 for r in validation_records if not r.is_compliant),
        "validation_records": [asdict(r) for r in validation_records]
    }
    manifest_path = os.path.join(out_dir, "validation_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(val_manifest, f, indent=2)
    print(f"Exported Validation Manifest: {manifest_path}")

    print("=== Python Processing Pipeline Successfully Concluded ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AX-CPT Python Psychometric Processing Pipeline")
    parser.add_argument("--config", default="config/pipeline_config.yaml", type=str, help="Path to pipeline_config.yaml")
    args = parser.parse_args()

    run_pipeline(args.config)
