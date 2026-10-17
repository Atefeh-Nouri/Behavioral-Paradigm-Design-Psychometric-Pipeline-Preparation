#!/usr/bin/env python3
r"""Master Repository Test Contract: Dual-Delay AX-Continuous Performance Test (cpt-project)

Root Directory: D:/Machine learning/Atefeh/cpt-project
Git Bash Equivalent: /d/Machine learning/Atefeh/cpt-project

This comprehensive test suite acts as the single source of truth for repository layout,
module imports, configuration contracts, run-rules, 22-column logging schema compliance,
Signal Detection Theory (SDT) mathematics, Median Absolute Deviation (MAD) cleaning logic,
and end-to-end integration contracts.
"""

import os
import sys
import math
import json
import traceback
import yaml
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import norm

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


# Helper for exception checking when pytest is not installed
def assert_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type as e:
        return e
    except Exception as e:
        raise AssertionError(f"Expected {exc_type.__name__}, but raised {type(e).__name__}: {e}")
    raise AssertionError(f"Expected {exc_type.__name__}, but no exception was raised.")


# =================================================================================================
# 1. ROOT PATH RESOLUTION & ENVIRONMENT SETUP
# =================================================================================================

def resolve_project_root() -> Path:
    """
    Resolves project root across Windows ('D:/Machine learning/Atefeh/cpt-project'),
    Git Bash ('/d/Machine learning/Atefeh/cpt-project'), or current working directory.
    """
    # 1. Check current working directory
    cwd = Path.cwd().resolve()
    if (cwd / "config" / "config.yaml").exists() or (cwd / "paradigms").exists():
        return cwd

    # 2. Check explicit Windows path
    win_path = Path(r"D:/Machine learning/Atefeh/cpt-project")
    if win_path.exists():
        return win_path.resolve()

    # 3. Check Git Bash / POSIX path
    gitbash_path = Path("/d/Machine learning/Atefeh/cpt-project")
    if gitbash_path.exists():
        return gitbash_path.resolve()

    # Fallback to cwd
    return cwd

PROJECT_ROOT = resolve_project_root()

# Ensure PROJECT_ROOT is on sys.path for robust package imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =================================================================================================
# 2. REPOSITORY STRUCTURE & FILE SYSTEM CONTRACTS
# =================================================================================================

def test_directory_structure_and_required_files():
    """
    Validates that all required package directories, configuration files,
    schema definitions, and documentation exist within the project root.
    """
    required_directories = [
        "config",
        "paradigms",
        "paradigms/psychopy",
        "paradigms/opensesame",
        "paradigms/opensesame/inline_scripts",
        "synthetic_data",
        "analysis_python",
        "analysis_r",
        "tests",
        "data/raw",
        "data/processed",
    ]

    for rel_dir in required_directories:
        dir_path = PROJECT_ROOT / rel_dir
        assert dir_path.exists(), f"Missing required directory: {rel_dir} at {dir_path}"
        assert dir_path.is_dir(), f"Expected directory but found file: {rel_dir}"

    required_files = [
        "config/config.yaml",
        "config/pipeline_config.yaml",
        "config/schema_raw_v1.json",
        "requirements.txt",
        ".gitignore",
        "README.md",
        "paradigms/psychopy/__init__.py",
        "paradigms/psychopy/config_loader.py",
        "paradigms/psychopy/engine.py",
        "paradigms/psychopy/trial_logic.py",
        "paradigms/psychopy/trial_executor.py",
        "paradigms/psychopy/ui.py",
        "paradigms/psychopy/logger.py",
        "paradigms/psychopy/main.py",
        "synthetic_data/__init__.py",
        "synthetic_data/generator.py",
        "synthetic_data/generate_benchmark.py",
        "analysis_python/__init__.py",
        "analysis_python/ingest.py",
        "analysis_python/clean.py",
        "analysis_python/sdt.py",
        "analysis_python/summarize.py",
        "analysis_python/cpt_pipeline.py",
    ]

    for rel_file in required_files:
        file_path = PROJECT_ROOT / rel_file
        assert file_path.exists(), f"Missing required file: {rel_file} at {file_path}"
        assert file_path.is_file(), f"Expected file but found directory: {rel_file}"


# =================================================================================================
# 3. CONFIGURATION CONTRACT VERIFICATION
# =================================================================================================

def test_master_experiment_config_contract():
    """
    Asserts every key and parameter bound in config/config.yaml against PSD v1.0 specifications.
    """
    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Core metadata
    assert cfg["version"] == "1.0.0"
    assert cfg["experiment_name"] == "dual_delay_ax_cpt"

    # Environment & Display Settings
    env = cfg["environment"]
    assert env["screen_number"] == 0
    assert env["fullscreen"] is True
    assert env["window_resolution"] == [1920, 1080]
    assert env["units"] == "height"
    assert env["target_refresh_hz"] == 60.0
    assert env["refresh_tolerance_hz"] == 1.0

    # Hardware Settings
    hw = cfg["hardware"]
    assert hw["keyboard_backend"] in ["ptb", "psychtoolbox", "iohub", "pynput"]
    assert hw["target_key"] == "space"
    assert hw["non_target_key"] == "l"
    assert hw["abort_key"] == "escape"

    # Millisecond Timing Chronometry
    tm = cfg["timing"]
    assert tm["fixation"]["nominal_ms"] == 500.0
    assert tm["fixation"]["jitter_min_ms"] == 400.0
    assert tm["fixation"]["jitter_max_ms"] == 600.0
    assert tm["stimulus"]["duration_ms"] == 300.0
    assert tm["stimulus"]["frames_at_60hz"] == 18
    assert tm["delays"]["short_delay_ms"] == 1200.0
    assert tm["delays"]["short_frames_at_60hz"] == 72
    assert tm["delays"]["long_delay_ms"] == 4000.0
    assert tm["delays"]["long_frames_at_60hz"] == 240
    assert tm["response_window_ms"] == 1000.0
    assert tm["iti"]["nominal_ms"] == 1200.0
    assert tm["iti"]["jitter_min_ms"] == 1000.0
    assert tm["iti"]["jitter_max_ms"] == 1400.0
    assert tm["anticipation_threshold_ms"] == 150.0

    # Experimental Design & Cell Distribution
    ds = cfg["design"]
    assert ds["total_blocks"] == 4
    assert ds["trials_per_block"] == 100
    assert ds["total_experimental_trials"] == 400
    assert ds["block_distribution"]["ax_count"] == 70
    assert ds["block_distribution"]["ay_count"] == 10
    assert ds["block_distribution"]["bx_count"] == 10
    assert ds["block_distribution"]["by_count"] == 10

    # Counterbalancing Groups
    cb = ds["counterbalancing_groups"]
    assert cb["group_a"] == ["SHORT_DELAY", "LONG_DELAY", "LONG_DELAY", "SHORT_DELAY"]
    assert cb["group_b"] == ["LONG_DELAY", "SHORT_DELAY", "SHORT_DELAY", "LONG_DELAY"]

    # Behavioral Run-Rules
    rr = ds["run_rules"]
    assert rr["max_consecutive_targets"] == 4
    assert rr["max_consecutive_nontargets"] == 2
    assert rr["no_consecutive_identical_distractors"] is True


def test_pipeline_config_contract():
    """
    Asserts cleaning rules, compliance thresholds, and Hautus SDT parameters in pipeline_config.yaml.
    """
    pipeline_cfg_path = PROJECT_ROOT / "config" / "pipeline_config.yaml"
    with open(pipeline_cfg_path, "r", encoding="utf-8") as f:
        p_cfg = yaml.safe_load(f)

    # Compliance Bounds
    comp = p_cfg["compliance_thresholds"]
    assert comp["min_trials_required"] == 380
    assert comp["max_ax_omission_rate"] == 0.15
    assert comp["max_anticipation_rate"] == 0.10

    # Latency Cleaning Rules
    clean = p_cfg["cleaning_rules"]
    assert clean["rt_cutoffs_ms"]["min"] == 150.0
    assert clean["rt_cutoffs_ms"]["max"] == 2000.0
    assert clean["mad_filtering"]["enabled"] is True
    assert clean["mad_filtering"]["threshold_k"] == 3.0
    assert abs(clean["mad_filtering"]["scale_constant"] - 1.4826022185056) < 1e-6

    # Signal Detection Parameters (Hautus 1995)
    sdt_p = p_cfg["sdt_parameters"]
    assert sdt_p["correction_method"] == "hautus_log_linear"
    assert sdt_p["hit_adjustment"] == 0.5
    assert sdt_p["total_signal_adjustment"] == 1.0
    assert sdt_p["fa_adjustment"] == 0.5
    assert sdt_p["total_noise_adjustment"] == 1.0


def test_raw_schema_json_contract():
    """
    Asserts JSONSchema specification for Raw Data Schema v1.0 (22 columns).
    """
    schema_path = PROJECT_ROOT / "config" / "schema_raw_v1.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    required_cols = schema.get("required", [])
    assert len(required_cols) == 22

    expected_cols = [
        "session_id", "participant_id", "block_index", "block_condition",
        "trial_index_global", "trial_index_block", "trial_type",
        "cue_stimulus", "probe_stimulus", "required_key",
        "cpi_nominal_ms", "cpi_realized_ms", "fixation_realized_ms",
        "probe_onset_timestamp", "response_key", "response_timestamp",
        "rt_ms", "is_correct", "outcome_code", "is_anticipation",
        "post_error_trial", "frame_drop_detected"
    ]
    assert required_cols == expected_cols


# =================================================================================================
# 4. PACKAGE MODULE IMPORTS CONTRACT
# =================================================================================================

def test_module_imports():
    """
    Verifies that all Python modules across paradigms, synthetic_data, and analysis_python
    can be imported cleanly without syntax errors or missing symbol definitions.
    """
    import paradigms.psychopy.config_loader as config_loader
    import paradigms.psychopy.trial_logic as trial_logic
    import paradigms.psychopy.logger as logger
    import synthetic_data.generator as generator
    import synthetic_data.generate_benchmark as generate_benchmark
    import analysis_python.ingest as ingest
    import analysis_python.clean as clean
    import analysis_python.sdt as sdt
    import analysis_python.summarize as summarize
    import analysis_python.cpt_pipeline as cpt_pipeline

    assert hasattr(config_loader, "load_experiment_config")
    assert hasattr(trial_logic, "TrialSequenceGenerator")
    assert hasattr(logger, "SessionDataLogger")
    assert hasattr(generator, "SyntheticDataGenerator")
    assert hasattr(generate_benchmark, "run_batch_generation")
    assert hasattr(ingest, "DataIngestor")
    assert hasattr(clean, "compute_within_subject_mad_bounds")
    assert hasattr(clean, "flag_trial_anomalies")
    assert hasattr(sdt, "calculate_hautus_sdt")
    assert hasattr(summarize, "summarize_subject_session")
    assert hasattr(cpt_pipeline, "run_pipeline")


# =================================================================================================
# 5. TRIAL GENERATOR & RUN-RULE ENGINE TESTS
# =================================================================================================

def test_trial_sequence_generator_and_run_rules():
    """
    Tests trial block generation for cell distribution (70/10/10/10) and run-rules:
    - Max 4 consecutive AX targets.
    - Max 2 consecutive non-target trials.
    - No identical consecutive distractors.
    """
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator

    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    gen = TrialSequenceGenerator(cfg, seed=2026)
    block = gen.generate_block("SHORT_DELAY")

    assert len(block) == 100

    # Cell Counts
    ax_trials = [t for t in block if t.trial_type == "AX"]
    ay_trials = [t for t in block if t.trial_type == "AY"]
    bx_trials = [t for t in block if t.trial_type == "BX"]
    by_trials = [t for t in block if t.trial_type == "BY"]

    assert len(ax_trials) == 70
    assert len(ay_trials) == 10
    assert len(bx_trials) == 10
    assert len(by_trials) == 10

    # Run-Rule Constraints Verification
    consec_ax = 0
    consec_nontarget = 0

    for i, t in enumerate(block):
        if t.trial_type == "AX":
            consec_ax += 1
            consec_nontarget = 0
        else:
            consec_nontarget += 1
            consec_ax = 0

        assert consec_ax <= 4, f"Violated max 4 consecutive AX targets at index {i}"
        assert consec_nontarget <= 2, f"Violated max 2 consecutive non-targets at index {i}"

        # Distractor Non-Repetition Rule
        if i > 0 and t.trial_type in ["BX", "BY"] and block[i - 1].trial_type in ["BX", "BY"]:
            assert t.cue_stimulus != block[i - 1].cue_stimulus, f"Consecutive invalid cue repeat at index {i}"
        if i > 0 and t.trial_type in ["AY", "BY"] and block[i - 1].trial_type in ["AY", "BY"]:
            assert t.probe_stimulus != block[i - 1].probe_stimulus, f"Consecutive invalid probe repeat at index {i}"


# =================================================================================================
# 6. LOGGING CONTRACT & SCHEMA VALIDATION TESTS
# =================================================================================================

def test_session_data_logger_schema_enforcement():
    """
    Verifies that SessionDataLogger strictly enforces the 22-column contract and catches errors.
    """
    from paradigms.psychopy.logger import SessionDataLogger, SchemaValidationError

    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    logger = SessionDataLogger("P_TEST", "A", cfg)
    assert len(logger.SCHEMA_COLUMNS) == 22

    # Truncated column test
    bad_df = pd.DataFrame([{"session_id": "123", "participant_id": "P_TEST"}])
    if HAS_PYTEST:
        with pytest.raises(SchemaValidationError) as exc_info:
            logger.validate_dataset(bad_df)
        assert "Column mismatch" in str(exc_info.value)
    else:
        err = assert_raises(SchemaValidationError, logger.validate_dataset, bad_df)
        assert "Column mismatch" in str(err)

    # Negative RT test
    records = []
    for i in range(1, 401):
        rec = {col: "null" for col in logger.SCHEMA_COLUMNS}
        rec["rt_ms"] = -50.0 if i == 1 else 400.0
        rec["outcome_code"] = "HIT"
        rec["is_anticipation"] = False
        records.append(rec)

    df_negative = pd.DataFrame(records)
    if HAS_PYTEST:
        with pytest.raises(SchemaValidationError) as exc_info:
            logger.validate_dataset(df_negative)
        assert "Negative reaction times detected" in str(exc_info.value)
    else:
        err = assert_raises(SchemaValidationError, logger.validate_dataset, df_negative)
        assert "Negative reaction times detected" in str(err)


# =================================================================================================
# 7. SIGNAL DETECTION THEORY (SDT) MATH TESTS
# =================================================================================================

def test_hautus_sdt_mathematical_precision():
    """
    Tests Hautus (1995) log-linear SDT calculation for hand-calculated cases and boundary zero rates.
    """
    from analysis_python.sdt import calculate_hautus_sdt

    # 1. Neutral Observer: 80% hits (80/100), 20% false alarms (20/100)
    # H_adj = 80.5 / 101.0 = 0.7970297
    # FA_adj = 20.5 / 101.0 = 0.2029703
    # Z(H_adj) = 0.83108, Z(FA_adj) = -0.83108
    # d' = 1.66216, c = 0.0
    d_prime, c, beta = calculate_hautus_sdt(hits=80, signal_trials=100, false_alarms=20, noise_trials=100)
    assert abs(d_prime - 1.66216) < 1e-3
    assert abs(c - 0.0) < 1e-3
    assert abs(beta - 1.0) < 1e-3

    # 2. Zero False Alarm Boundary Case: 100% hits (100/100), 0% false alarms (0/100)
    # H_adj = 100.5 / 101.0 = 0.9950495
    # FA_adj = 0.5 / 101.0 = 0.0049505
    # Z(H_adj) = 2.57829, Z(FA_adj) = -2.57829
    # d' = 5.15658, c = 0.0
    d_zero_fa, c_zero_fa, _ = calculate_hautus_sdt(hits=100, signal_trials=100, false_alarms=0, noise_trials=100)
    assert not math.isinf(d_zero_fa)
    assert not math.isnan(d_zero_fa)
    assert abs(d_zero_fa - 5.15854) < 1e-2
    assert abs(c_zero_fa - 0.0) < 1e-3


# =================================================================================================
# 8. MAD OUTLIER FILTERING TESTS
# =================================================================================================

def test_mad_latency_filtering():
    """
    Verifies within-subject MAD bound calculation and non-destructive flagging.
    """
    from analysis_python.clean import compute_within_subject_mad_bounds, flag_trial_anomalies

    # Normal distribution with 1 extreme outlier
    np.random.seed(42)
    normal_rts = list(np.random.normal(400.0, 20.0, 99))
    normal_rts.append(1999.0)  # Extreme lapse outlier

    dummy_df = pd.DataFrame({"rt_ms": normal_rts})
    low_b, high_b = compute_within_subject_mad_bounds(dummy_df, k=3.0)

    assert low_b >= 150.0
    assert high_b < 600.0  # MAD bound resists extreme outlier tail

    # Non-destructive flagging contract check
    pipeline_cfg_path = PROJECT_ROOT / "config" / "pipeline_config.yaml"
    with open(pipeline_cfg_path, "r", encoding="utf-8") as f:
        p_cfg = yaml.safe_load(f)

    dummy_trials = pd.DataFrame({
        "participant_id": ["P001"] * 10,
        "trial_type": ["AX"] * 10,
        "is_correct": [True] * 10,
        "flag_duplicate_row": [False] * 10,
        "rt_ms": [100.0, 350.0, 360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 2500.0]
    })

    flagged_df = flag_trial_anomalies(dummy_trials, p_cfg)

    assert len(flagged_df) == 10  # Zero rows dropped
    assert flagged_df.loc[0, "flag_anticipation"] is True or flagged_df.loc[0, "flag_anticipation"] == 1
    assert flagged_df.loc[9, "flag_absolute_outlier"] is True or flagged_df.loc[9, "flag_absolute_outlier"] == 1


# =================================================================================================
# 9. END-TO-END INTEGRATION TEST
# =================================================================================================

def test_end_to_end_synthetic_generation_and_pipeline():
    """
    Runs single-subject synthetic generation, verifies raw output schema,
    routes through DataIngestor to attach audit flags, and executes 
    Python psychometric cleaning and summarization.
    """
    from synthetic_data.generator import SyntheticDataGenerator
    from paradigms.psychopy.trial_logic import TrialSequenceGenerator
    from analysis_python.ingest import DataIngestor
    from analysis_python.clean import flag_trial_anomalies
    from analysis_python.summarize import summarize_subject_session

    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        
    pipeline_cfg_path = PROJECT_ROOT / "config" / "pipeline_config.yaml"
    with open(pipeline_cfg_path, "r", encoding="utf-8") as f:
        p_cfg = yaml.safe_load(f)

    # 1. Generate Single Subject
    generator = SyntheticDataGenerator(cfg, master_seed=42)
    seq_gen = TrialSequenceGenerator(cfg, seed=42)
    traits = generator.draw_subject_traits("SUBJ_001")
    
    trials = []
    global_idx = 1
    is_post_error = False
    block_conditions = cfg["design"]["counterbalancing_groups"]["group_a"]
    subj_rng = np.random.default_rng(42)

    for b_idx, condition in enumerate(block_conditions, start=1):
        b_trials = seq_gen.generate_block(condition)
        for b_t_idx, t_def in enumerate(b_trials, start=1):
            t_dict = {
                "session_id": "test-uuid-42",
                "participant_id": "SUBJ_001",
                "block_index": b_idx,
                "block_condition": condition,
                "trial_index_block": b_t_idx,
                "trial_type": t_def.trial_type,
                "cue_stimulus": t_def.cue_stimulus,
                "probe_stimulus": t_def.probe_stimulus,
                "required_key": t_def.required_key,
                "cpi_nominal_ms": t_def.cpi_nominal_ms,
            }
            
            # Correct argument order based on generate_benchmark.py
            res = generator.simulate_trial(
                traits=traits,
                trial_def=t_dict,
                trial_idx=global_idx,
                is_post_error=is_post_error,
                rng=subj_rng
            )
            
            trials.append(res)
            is_post_error = not res["is_correct"]
            global_idx += 1
            
    df_raw = pd.DataFrame(trials)
    assert len(df_raw) == 400

    # 2. Route through DataIngestor (populates flag_duplicate_row / flag_dropped_trial)
    # This satisfies the "DEFENSIVE DATA CONTRACT INITIALIZATION" requirement in clean.py
    ingestor = DataIngestor(str(pipeline_cfg_path))
    df_ingested, _ = ingestor.audit_subject_session(df_raw, "in_memory_test.csv")

    # 3. Clean & Flag Anomalies
    df_cleaned = flag_trial_anomalies(df_ingested, p_cfg)
    assert len(df_cleaned) == 400
    assert "is_retained_for_rt" in df_cleaned.columns
    assert "is_retained_for_sdt" in df_cleaned.columns

    # 4. Summarize Subject
    summary = summarize_subject_session(df_cleaned, is_compliant=True, rejection_reason="NONE")
    assert summary["participant_id"] == "SUBJ_001"
    assert summary["n_trials_raw"] == 400
    assert 0.0 <= summary["ax_hit_rate"] <= 1.0
    assert 0.0 <= summary["ay_commission_rate"] <= 1.0
    assert summary["dprime_global"] > 0.0
    assert summary["dprime_context"] > 0.0


# =================================================================================================
# MAIN RUNNER FOR DIRECT PYTHON EXECUTION
# =================================================================================================

if __name__ == "__main__":
    print(f"=== Running Master Repository Test Contract ===")
    print(f"Project Root Resolved To: {PROJECT_ROOT}\n")

    test_functions = [
        ("Directory & File Structure", test_directory_structure_and_required_files),
        ("Master Experiment Configuration Contract", test_master_experiment_config_contract),
        ("Pipeline Configuration Contract", test_pipeline_config_contract),
        ("Raw Data Schema v1.0 Contract", test_raw_schema_json_contract),
        ("Package & Module Imports", test_module_imports),
        ("Trial Sequence Generator & Run-Rules Engine", test_trial_sequence_generator_and_run_rules),
        ("Session Data Logger & Schema Validation", test_session_data_logger_schema_enforcement),
        ("Hautus SDT Mathematical Precision", test_hautus_sdt_mathematical_precision),
        ("MAD Latency Outlier Filtering", test_mad_latency_filtering),
        ("End-to-End Synthetic Generation & Pipeline", test_end_to_end_synthetic_generation_and_pipeline),
    ]

    passed = 0
    failed = 0

    for name, test_func in test_functions:
        try:
            test_func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            traceback.print_exc()
            print(f"[FAIL] {name}: {e}")
            failed += 1

    print(f"\nTest Summary: {passed} PASSED, {failed} FAILED")
    if failed > 0:
        sys.exit(1)
    else:
        print("ALL TESTS PASSED PERFECTLY!")
        sys.exit(0)