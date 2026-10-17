"""
Trial Sequence Generator and Run-Rule Tests.
Verifies bounded rejection sampling, cell balancing, and run-rule constraints.
"""

import os
import pytest
import yaml

try:
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator


@pytest.fixture
def base_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_block_generation_distribution(base_config):
    """Verifies that each 100-trial block adheres exactly to the 70/10/10/10 distribution."""
    gen = TrialSequenceGenerator(base_config, seed=42)
    block = gen.generate_block("SHORT_DELAY")

    assert len(block) == 100
    ax_trials = [t for t in block if t.trial_type == "AX"]
    ay_trials = [t for t in block if t.trial_type == "AY"]
    bx_trials = [t for t in block if t.trial_type == "BX"]
    by_trials = [t for t in block if t.trial_type == "BY"]

    assert len(ax_trials) == 70
    assert len(ay_trials) == 10
    assert len(bx_trials) == 10
    assert len(by_trials) == 10


def test_run_rules_satisfaction(base_config):
    """Verifies run-rule satisfaction: max 4 consecutive AX, max 2 non-targets, no distractor repeats."""
    gen = TrialSequenceGenerator(base_config, seed=123)
    block = gen.generate_block("LONG_DELAY")

    consec_ax = 0
    consec_nontarget = 0

    for i, trial in enumerate(block):
        if trial.trial_type == "AX":
            consec_ax += 1
            consec_nontarget = 0
        else:
            consec_nontarget += 1
            consec_ax = 0

        assert consec_ax <= 4, f"Violated max 4 consecutive AX trials at trial {i}"
        assert consec_nontarget <= 2, f"Violated max 2 consecutive non-targets at trial {i}"

        # Distractor non-repetition
        if i > 0 and trial.trial_type in ["BX", "BY"] and block[i - 1].trial_type in ["BX", "BY"]:
            assert trial.cue_stimulus != block[i - 1].cue_stimulus, "Repeated consecutive invalid cue"
        if i > 0 and trial.trial_type in ["AY", "BY"] and block[i - 1].trial_type in ["AY", "BY"]:
            assert trial.probe_stimulus != block[i - 1].probe_stimulus, "Repeated consecutive invalid probe"


def test_deterministic_reproducibility(base_config):
    """Verifies that identical seeds yield identical trial sequences."""
    gen1 = TrialSequenceGenerator(base_config, seed=999)
    gen2 = TrialSequenceGenerator(base_config, seed=999)

    block1 = gen1.generate_block("SHORT_DELAY")
    block2 = gen2.generate_block("SHORT_DELAY")

    for t1, t2 in zip(block1, block2):
        assert t1.trial_type == t2.trial_type
        assert t1.cue_stimulus == t2.cue_stimulus
        assert t1.probe_stimulus == t2.probe_stimulus
