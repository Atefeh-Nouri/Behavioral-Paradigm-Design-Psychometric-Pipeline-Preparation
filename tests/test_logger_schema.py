"""
Logger Contract and Schema Conformance Tests.
Asserts that SessionDataLogger strictly produces 22-column records matching Raw Data Schema v1.0.
"""

import json
import os
import pytest
import pandas as pd
import yaml

try:
    from paradigms.psychopy.logger import SessionDataLogger, SchemaValidationError
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from paradigms.psychopy.logger import SessionDataLogger, SchemaValidationError


@pytest.fixture
def config_and_logger():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    logger = SessionDataLogger("P_TEST", "A", cfg)
    return cfg, logger


def test_schema_column_names(config_and_logger):
    """Verifies logger adheres exactly to the 22 columns in Raw Data Schema v1.0."""
    _, logger = config_and_logger
    assert len(logger.SCHEMA_COLUMNS) == 22
    assert logger.SCHEMA_COLUMNS[0] == "session_id"
    assert logger.SCHEMA_COLUMNS[-1] == "frame_drop_detected"


def test_schema_validator_catches_missing_columns(config_and_logger):
    """Verifies that validate_dataset raises SchemaValidationError on truncated columns."""
    _, logger = config_and_logger
    bad_df = pd.DataFrame([{"session_id": "123", "participant_id": "P_TEST"}])

    with pytest.raises(SchemaValidationError) as exc_info:
        logger.validate_dataset(bad_df)
    assert "Column mismatch" in str(exc_info.value)


def test_schema_validator_catches_negative_rts(config_and_logger):
    """Verifies that negative reaction times trigger validation failure."""
    cfg, logger = config_and_logger
    # Construct dummy 400 rows
    records = []
    for i in range(1, 401):
        rec = {col: "null" for col in logger.SCHEMA_COLUMNS}
        rec["rt_ms"] = -50.0 if i == 1 else 400.0
        rec["outcome_code"] = "HIT"
        rec["is_anticipation"] = False
        records.append(rec)

    df_negative = pd.DataFrame(records)
    with pytest.raises(SchemaValidationError) as exc_info:
        logger.validate_dataset(df_negative)
    assert "Negative reaction times detected" in str(exc_info.value)
