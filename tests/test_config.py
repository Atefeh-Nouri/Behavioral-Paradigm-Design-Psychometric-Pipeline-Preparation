"""
Configuration Schema and Value Bounds Tests.
Asserts that config.yaml and pipeline_config.yaml conform to expected models and constraints.
"""

import os
import pytest
import yaml

try:
    from paradigms.psychopy.config_loader import load_experiment_config, ExperimentConfig
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from paradigms.psychopy.config_loader import load_experiment_config, ExperimentConfig


def test_experiment_config_validity():
    """Verifies that config/config.yaml parses and satisfies all field constraints."""
    config_path = "config/config.yaml"
    assert os.path.exists(config_path), f"Missing config file: {config_path}"

    cfg = load_experiment_config(config_path)
    assert isinstance(cfg, dict)

    # Assert structural parameters
    assert cfg["timing"]["stimulus"]["duration_ms"] == 300.0
    assert cfg["timing"]["delays"]["short_delay_ms"] == 1200.0
    assert cfg["timing"]["delays"]["long_delay_ms"] == 4000.0
    assert cfg["timing"]["response_window_ms"] == 1000.0
    assert cfg["timing"]["anticipation_threshold_ms"] == 150.0
    assert cfg["design"]["total_experimental_trials"] == 400
    assert cfg["design"]["block_distribution"]["ax_count"] == 70


def test_pipeline_config_validity():
    """Verifies that config/pipeline_config.yaml has valid cleaning thresholds and SDT settings."""
    pipeline_cfg_path = "config/pipeline_config.yaml"
    assert os.path.exists(pipeline_cfg_path), f"Missing pipeline config: {pipeline_cfg_path}"

    with open(pipeline_cfg_path, "r", encoding="utf-8") as f:
        p_cfg = yaml.safe_load(f)

    assert p_cfg["compliance_thresholds"]["min_trials_required"] == 380
    assert p_cfg["compliance_thresholds"]["max_ax_omission_rate"] == 0.15
    assert p_cfg["cleaning_rules"]["mad_filtering"]["threshold_k"] == 3.0
    assert p_cfg["sdt_parameters"]["correction_method"] == "hautus_log_linear"
    assert p_cfg["sdt_parameters"]["hit_adjustment"] == 0.5
    assert p_cfg["sdt_parameters"]["total_signal_adjustment"] == 1.0
