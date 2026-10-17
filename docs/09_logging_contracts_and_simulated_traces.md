# Logging Hardening & Output Schema Traces (Day 9)

## 1. Schema Enforcement Architecture
`SessionDataLogger` enforces column structure, data types, nullability, and allowed values before writing to disk. Sessions are cryptographically stamped with SHA-256 configuration hashes.

## 2. Simulated Session Output Traces (`P001_trials.csv`)

### Hit Trial (AX Target)
```csv
session_id,participant_id,block_index,block_condition,trial_index_global,trial_index_block,trial_type,cue_stimulus,probe_stimulus,required_key,cpi_nominal_ms,cpi_realized_ms,fixation_realized_ms,probe_onset_timestamp,response_key,response_timestamp,rt_ms,is_correct,outcome_code,is_anticipation,post_error_trial,frame_drop_detected
9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d,P001,1,SHORT_DELAY,1,1,AX,A,X,space,1200.0,1200.124,512.401,14.82103,space,15.18341,362.380,True,HIT,False,False,False
```

### Anticipation Trial (AY Conflict)
```csv
session_id,participant_id,block_index,block_condition,trial_index_global,trial_index_block,trial_type,cue_stimulus,probe_stimulus,required_key,cpi_nominal_ms,cpi_realized_ms,fixation_realized_ms,probe_onset_timestamp,response_key,response_timestamp,rt_ms,is_correct,outcome_code,is_anticipation,post_error_trial,frame_drop_detected
9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d,P001,1,SHORT_DELAY,2,2,AY,A,S,l,1200.0,1199.982,488.112,18.23412,space,18.32412,90.000,False,ANTICIPATION,True,False,False
```

### Omission Error (BX Long Delay)
```csv
session_id,participant_id,block_index,block_condition,trial_index_global,trial_index_block,trial_type,cue_stimulus,probe_stimulus,required_key,cpi_nominal_ms,cpi_realized_ms,fixation_realized_ms,probe_onset_timestamp,response_key,response_timestamp,rt_ms,is_correct,outcome_code,is_anticipation,post_error_trial,frame_drop_detected
9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d,P001,2,LONG_DELAY,101,1,BX,C,X,l,4000.0,4000.311,540.211,412.19342,,,None,False,OMISSION_ERROR,False,True,False
```