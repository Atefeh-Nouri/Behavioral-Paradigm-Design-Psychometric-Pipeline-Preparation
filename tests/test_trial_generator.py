"""
Unit tests for pure-Python AX-CPT trial sequence generation.

These tests deliberately load `trial_logic.py` directly from file path so that
they do not trigger `paradigms.psychopy.__init__.py`.

This makes the test CI-safe even when PsychoPy/PsychToolbox are not installed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import pytest


ROOT = Path(__file__).resolve().parents[1]
TRIAL_LOGIC_PATH = ROOT / "paradigms" / "psychopy" / "trial_logic.py"


def _load_trial_logic_module():
    """
    Load trial_logic.py as an isolated module.

    This avoids executing paradigms/psychopy/__init__.py, which may import
    PsychoPy-dependent engine/UI modules.
    """

    spec = importlib.util.spec_from_file_location(
        "cpt_trial_logic_isolated",
        TRIAL_LOGIC_PATH,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not create import spec for: {TRIAL_LOGIC_PATH}"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


trial_logic = _load_trial_logic_module()

TrialSequenceGenerator = trial_logic.TrialSequenceGenerator
TrialDefinition = trial_logic.TrialDefinition


@pytest.fixture(scope="module")
def base_config() -> Dict[str, Any]:
    """
    Minimal canonical AX-CPT configuration for generator tests.

    This mirrors the expected production config structure but stays small
    and deterministic.
    """

    return {
        "timing": {
            "delays": {
                "short_delay_ms": 1500,
                "long_delay_ms": 5000,
            }
        },
        "hardware": {
            "target_key": "f",
            "non_target_key": "j",
        },
        "stimuli": {
            "target_cue": "A",
            "target_probe": "X",
            "distractor_cue": "B",
            "distractor_probe": "Y",
        },
        "design": {
            "random_seed": 2026,
            "max_generation_attempts": 5000,
            "block_distribution": {
                "ax_count": 70,
                "ay_count": 10,
                "bx_count": 10,
                "by_count": 10,
            },
            "run_rules": {
                "max_consecutive_targets": 4,
                "max_consecutive_nontargets": 2,
                "no_consecutive_identical_distractors": True,
            },
        },
    }


def _type_counts(block: List[Any]) -> Dict[str, int]:
    counts = {
        "AX": 0,
        "AY": 0,
        "BX": 0,
        "BY": 0,
    }

    for trial in block:
        counts[trial.trial_type] += 1

    return counts


def _max_run(
    block: List[Any],
    predicate: Callable[[Any], bool],
) -> int:
    max_run = 0
    current = 0

    for trial in block:
        if predicate(trial):
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0

    return max_run


def _serialize_block(
    block: List[Any],
) -> List[Tuple[str, str, str, str, float, str]]:
    return [
        (
            trial.trial_type,
            trial.cue_stimulus,
            trial.probe_stimulus,
            trial.required_key,
            trial.cpi_nominal_ms,
            trial.block_condition,
        )
        for trial in block
    ]


def test_trial_logic_source_has_no_psychopy_import() -> None:
    """
    Guards against reintroducing a hard PsychoPy dependency into trial_logic.py.
    """

    source = TRIAL_LOGIC_PATH.read_text(encoding="utf-8")
    normalized = source.replace("\r\n", "\n")

    assert "from psychopy" not in normalized
    assert "import psychopy" not in normalized


def test_generate_block_short_delay_structure(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=999)
    block = generator.generate_block("SHORT_DELAY")

    assert len(block) == 100
    assert all(isinstance(trial, TrialDefinition) for trial in block)

    counts = _type_counts(block)

    assert counts == {
        "AX": 70,
        "AY": 10,
        "BX": 10,
        "BY": 10,
    }

    assert all(trial.block_condition == "SHORT_DELAY" for trial in block)
    assert all(trial.cpi_nominal_ms == 1500.0 for trial in block)


def test_generate_block_long_delay_cpi(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=999)
    block = generator.generate_block("LONG_DELAY")

    assert len(block) == 100
    assert all(trial.block_condition == "LONG_DELAY" for trial in block)
    assert all(trial.cpi_nominal_ms == 5000.0 for trial in block)


def test_required_keys_match_trial_type(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=123)
    block = generator.generate_block("SHORT_DELAY")

    for trial in block:
        if trial.trial_type == "AX":
            assert trial.required_key == "f"
        else:
            assert trial.required_key == "j"


def test_stimulus_mapping_is_canonical(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=123)
    block = generator.generate_block("SHORT_DELAY")

    expected = {
        "AX": ("A", "X"),
        "AY": ("A", "Y"),
        "BX": ("B", "X"),
        "BY": ("B", "Y"),
    }

    for trial in block:
        assert (
            trial.cue_stimulus,
            trial.probe_stimulus,
        ) == expected[trial.trial_type]


def test_max_consecutive_target_run_is_respected(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=777)
    block = generator.generate_block("SHORT_DELAY")

    max_ax_run = _max_run(
        block,
        predicate=lambda trial: trial.trial_type == "AX",
    )

    assert max_ax_run <= 4


def test_max_consecutive_nontarget_run_is_respected(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=777)
    block = generator.generate_block("SHORT_DELAY")

    max_non_run = _max_run(
        block,
        predicate=lambda trial: trial.trial_type != "AX",
    )

    assert max_non_run <= 2


def test_no_consecutive_identical_distractors(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=4242)
    block = generator.generate_block("SHORT_DELAY")

    for idx in range(1, len(block)):
        prev = block[idx - 1]
        curr = block[idx]

        if (
            curr.trial_type in ("BX", "BY")
            and prev.trial_type in ("BX", "BY")
        ):
            assert curr.cue_stimulus != prev.cue_stimulus

        if (
            curr.trial_type in ("AY", "BY")
            and prev.trial_type in ("AY", "BY")
        ):
            assert curr.probe_stimulus != prev.probe_stimulus


def test_internal_run_rule_validator_accepts_generated_block(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=31337)
    block = generator.generate_block("SHORT_DELAY")

    assert generator._satisfies_run_rules(block) is True


def test_same_seed_is_deterministic(
    base_config: Dict[str, Any],
) -> None:
    block_a = TrialSequenceGenerator(base_config, seed=555).generate_block(
        "SHORT_DELAY"
    )
    block_b = TrialSequenceGenerator(base_config, seed=555).generate_block(
        "SHORT_DELAY"
    )

    assert _serialize_block(block_a) == _serialize_block(block_b)


def test_generator_can_be_reused_with_different_conditions(
    base_config: Dict[str, Any],
) -> None:
    generator = TrialSequenceGenerator(base_config, seed=8080)

    short_block = generator.generate_block("SHORT_DELAY")
    long_block = generator.generate_block("LONG_DELAY")

    assert len(short_block) == 100
    assert len(long_block) == 100

    assert all(t.block_condition == "SHORT_DELAY" for t in short_block)
    assert all(t.block_condition == "LONG_DELAY" for t in long_block)

    assert all(t.cpi_nominal_ms == 1500.0 for t in short_block)
    assert all(t.cpi_nominal_ms == 5000.0 for t in long_block)