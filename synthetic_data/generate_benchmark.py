"""
Batch Generation Engine for Benchmark Dataset v1.0 (Deliverable D5).
Produces N=50 subjects x 400 trials conforming to Raw Data Schema v1.0,
alongside a ground-truth parameter registry and cryptographic manifest.
"""

import argparse
import hashlib
import json
import os
import sys
import uuid
import numpy as np
import pandas as pd
import yaml

# Cross-module import support
try:
    from synthetic_data.generator import SyntheticDataGenerator, SubjectTraits, inject_dataset_anomalies
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from synthetic_data.generator import SyntheticDataGenerator, SubjectTraits, inject_dataset_anomalies
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator


def run_batch_generation(config_path: str = "config/config.yaml", master_seed: int = 2026):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    out_dir = config["logging"]["output_dir"]
    os.makedirs(out_dir, exist_ok=True)

    generator = SyntheticDataGenerator(config, master_seed=master_seed)
    seq_gen = TrialSequenceGenerator(config, seed=master_seed)

    ground_truth_records = []
    manifest_files = {}

    print(f"=== Starting Batch Benchmark Generation (N=50 Subjects, Master Seed={master_seed}) ===")

    for s_idx in range(1, 51):
        subj_id = f"SUBJ_{s_idx:03d}"
        is_stress = (s_idx == 50)  # Reserve subject 50 as the stress-test case
        group = "A" if (s_idx % 2 == 1) else "B"

        # 1. Sample Subject Latent Traits
        traits = generator.draw_subject_traits(subj_id, is_stress_case=is_stress)

        # Log ground truth for psychometric recovery evaluation
        ground_truth_records.append({
            "participant_id": subj_id,
            "group": group,
            "is_stress_case": traits.is_stress_case,
            "true_mu": round(traits.mu, 3),
            "true_sigma": round(traits.sigma, 3),
            "true_tau": round(traits.tau, 3),
            "true_d_prime": round(traits.d_prime, 3),
            "true_criterion": round(traits.criterion, 3),
            "true_beta_mu": round(traits.beta_mu, 3),
            "true_beta_tau": round(traits.beta_tau, 3),
            "true_pes_ms": round(traits.pes_ms, 3),
            "true_p_anticipation": round(traits.p_anticipation, 4),
            "true_p_omission": round(traits.p_omission, 4)
        })

        # 2. Generate Counterbalanced Blocks
        group_key = f"group_{group.lower()}"
        block_conditions = config["design"]["counterbalancing_groups"][group_key]

        subj_trials = []
        global_idx = 1
        is_post_error = False
        subj_rng = np.random.default_rng(master_seed + s_idx)
        session_uuid = str(uuid.UUID(int=int(subj_rng.integers(0, 2**128))))

        for b_idx, cond in enumerate(block_conditions, start=1):
            block_defs = seq_gen.generate_block(cond)
            for b_trial_idx, t_def in enumerate(block_defs, start=1):
                raw_def = {
                    "session_id": session_uuid,
                    "participant_id": subj_id,
                    "block_index": b_idx,
                    "block_condition": cond,
                    "trial_index_block": b_trial_idx,
                    "trial_type": t_def.trial_type,
                    "cue_stimulus": t_def.cue_stimulus,
                    "probe_stimulus": t_def.probe_stimulus,
                    "required_key": t_def.required_key,
                    "cpi_nominal_ms": t_def.cpi_nominal_ms
                }
                trial_res = generator.simulate_trial(traits, raw_def, global_idx, is_post_error, subj_rng)
                subj_trials.append(trial_res)
                is_post_error = not trial_res["is_correct"]
                global_idx += 1

        df_subj = pd.DataFrame(subj_trials)

        # 3. Inject Technical and Dataset Anomalies
        df_subj = inject_dataset_anomalies(df_subj, subj_id, subj_rng)

        # 4. Save Participant CSV
        csv_filename = f"{subj_id}_raw_trials.csv"
        csv_path = os.path.join(out_dir, csv_filename)
        df_subj.to_csv(csv_path, index=False)

        # Compute file checksum
        with open(csv_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        manifest_files[csv_filename] = {
            "participant_id": subj_id,
            "rows": len(df_subj),
            "sha256": file_hash
        }

    # Save Ground Truth
    df_gt = pd.DataFrame(ground_truth_records)
    gt_path = os.path.join(out_dir, "benchmark_ground_truth.csv")
    df_gt.to_csv(gt_path, index=False)
    with open(gt_path, "rb") as f:
        gt_hash = hashlib.sha256(f.read()).hexdigest()

    # Save Manifest
    manifest = {
        "dataset_name": "AX-CPT Synthetic Benchmark v1.0",
        "deliverable": "D5",
        "num_subjects": 50,
        "master_seed": master_seed,
        "config_hash": hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
        "ground_truth_sha256": gt_hash,
        "files": manifest_files
    }
    manifest_path = os.path.join(out_dir, "benchmark_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"=== Benchmark Generation Complete. Saved 50 subjects to {out_dir} ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AX-CPT Benchmark Dataset v1.0")
    parser.add_argument("--config", default="config/config.yaml", type=str, help="Path to config.yaml")
    parser.add_argument("--seed", default=2026, type=int, help="Master RNG seed")
    args = parser.parse_args()

    run_batch_generation(config_path=args.config, master_seed=args.seed)
