"""
OpenSesame Trial Scoring and Schema Contract Enforcement.
Executed in the 'Run' phase of 'score_trial'.
Categorizes outcomes, isolates anticipations (<150 ms), and populates 22-column contract.
"""

# Input variables from OpenSesame keyboard_response
raw_rt = var.response_time
resp_key = var.response
req_key = var.required_key

# Outcome categorization
is_anticipation = False
rt_ms = None
response_key_logged = None
response_ts = None

if resp_key is None or resp_key == "None" or resp_key == "timeout":
    outcome_code = "OMISSION_ERROR"
    is_correct = False
else:
    response_key_logged = str(resp_key).lower()
    rt_ms = float(raw_rt)
    response_ts = round((var.time_probe_sketchpad + rt_ms) / 1000.0, 5)

    if rt_ms < 150.0:
        is_anticipation = True
        outcome_code = "ANTICIPATION"
        is_correct = (response_key_logged == req_key)
    elif response_key_logged == req_key:
        outcome_code = "HIT" if var.trial_type == "AX" else "CORRECT_REJECTION"
        is_correct = True
    else:
        outcome_code = "COMMISSION_ERROR"
        is_correct = False

# Compute realized chronometry
cpi_realized_ms = round(float(var.time_probe_sketchpad - var.time_cue_sketchpad), 3)
fixation_realized_ms = round(float(var.time_cue_sketchpad - var.time_fixation_sketchpad), 3)
probe_onset_ts = round(float(var.time_probe_sketchpad) / 1000.0, 5)

# Map directly to Raw Data Schema v1.0 logger variables
var.col_session_id = exp.vars.session_id
var.col_participant_id = exp.vars.participant_id
var.col_block_index = int(var.block_nr)
var.col_block_condition = var.block_condition
var.col_trial_index_global = int(var.trial_index_global)
var.col_trial_index_block = int(var.trial_index_block)
var.col_trial_type = var.trial_type
var.col_cue_stimulus = var.cue_stimulus
var.col_probe_stimulus = var.probe_stimulus
var.col_required_key = req_key
var.col_cpi_nominal_ms = float(var.cpi_nominal_ms)
var.col_cpi_realized_ms = cpi_realized_ms
var.col_fixation_realized_ms = fixation_realized_ms
var.col_probe_onset_timestamp = probe_onset_ts
var.col_response_key = response_key_logged if response_key_logged else "null"
var.col_response_timestamp = response_ts if response_ts else "null"
var.col_rt_ms = round(rt_ms, 3) if rt_ms is not None else "null"
var.col_is_correct = bool(is_correct)
var.col_outcome_code = outcome_code
var.col_is_anticipation = bool(is_anticipation)
var.col_post_error_trial = bool(var.post_error_trial)
var.col_frame_drop_detected = False

# Update state machine for next cycle
exp.vars.is_post_error = not is_correct
exp.vars.global_trial_index += 1
