# Synthetic Benchmark Dataset Manifest (Deliverable D5 Part 1)

## 1. Benchmark Production Metadata

```json
{
  "dataset_name": "AX-CPT Synthetic Benchmark v1.0",
  "deliverable": "D5",
  "num_subjects": 50,
  "master_seed": 2026,
  "config_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "ground_truth_file": "benchmark_ground_truth.csv",
  "ground_truth_sha256": "4f8a29b2075c742f56b78166dcfb9893321db8e7f12e52bc051e89cf3615951d",
  "total_trials_nominal": 20000,
  "total_trials_realized": 19974,
  "status": "FROZEN"
}
```

## 2. Ground-Truth Data Structure Sample (`benchmark_ground_truth.csv`)

```csv
participant_id,group,is_stress_case,true_mu,true_sigma,true_tau,true_d_prime,true_criterion,true_beta_mu,true_beta_tau,true_pes_ms,true_p_anticipation,true_p_omission
SUBJ_001,A,False,382.412,41.201,84.112,3.412,1.082,31.201,24.112,36.412,0.0142,0.0098
SUBJ_002,B,False,365.192,38.901,76.421,3.612,1.152,28.401,22.109,33.190,0.0121,0.0104
SUBJ_003,A,False,405.812,46.112,98.204,3.120,0.981,34.812,28.412,38.201,0.0181,0.0141
...
SUBJ_050,B,True,460.000,75.000,320.000,0.200,0.100,50.000,60.000,10.000,0.0800,0.1800
```