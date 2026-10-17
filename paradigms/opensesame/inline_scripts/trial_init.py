"""
OpenSesame Trial Initialization Inline Script.
Executed in the 'Run' phase of 'trial_init'.
Pops current trial definition, computes jitter, and assigns sketchpad variables.
"""

import random

# Retrieve current block trial definition
current_block = exp.vars.current_block_trials
block_trial_idx = var.count_trial_sequence  # 0-indexed trial count in loop

t_def = current_block[block_trial_idx]

# Stimulus identity
var.trial_type = t_def.trial_type
var.cue_stimulus = t_def.cue_stimulus
var.probe_stimulus = t_def.probe_stimulus
var.required_key = t_def.required_key
var.cpi_nominal_ms = int(t_def.cpi_nominal_ms)
var.block_condition = t_def.block_condition

# Timing jitter
fix_cfg = exp.vars.config["timing"]["fixation"]
var.fixation_duration_ms = int(random.uniform(fix_cfg["jitter_min_ms"], fix_cfg["jitter_max_ms"]))

# Internal telemetry tracking
var.trial_index_global = exp.vars.global_trial_index
var.trial_index_block = block_trial_idx + 1
var.post_error_trial = exp.vars.is_post_error
