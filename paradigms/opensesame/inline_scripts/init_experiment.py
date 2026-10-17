"""
OpenSesame Initialization Inline Script.
Executed in the 'Run' phase of 'init_experiment'.
Loads centralized configuration, initializes tracking UUIDs, and sets counterbalancing.
"""

import os
import uuid
import yaml

# Resolve project root relative to experiment file
exp_dir = exp.experiment_path
config_path = os.path.join(exp_dir, "..", "..", "config", "config.yaml")
config_path = os.path.abspath(config_path)

if not os.path.exists(config_path):
    # Fallback to local working directory
    config_path = os.path.abspath("config/config.yaml")

with open(config_path, "r", encoding="utf-8") as f:
    exp.vars.config = yaml.safe_load(f)

# Establish session telemetry
exp.vars.session_id = str(uuid.uuid4())
exp.vars.participant_id = f"SUBJ_{int(var.subject_nr):03d}"
exp.vars.global_trial_index = 1
exp.vars.is_post_error = False

# Assign counterbalancing group (Group A: Odd subjects, Group B: Even subjects)
subj_int = int(var.subject_nr)
group_name = "A" if (subj_int % 2 == 1) else "B"
group_key = f"group_{group_name.lower()}"
exp.vars.assigned_group = group_name
exp.vars.block_conditions = exp.vars.config["design"]["counterbalancing_groups"][group_key]

print(f"[OpenSesame Init] Subject: {exp.vars.participant_id} | Group: {group_name} | Session: {exp.vars.session_id}")
