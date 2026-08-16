from src.data.load_data import load_data
from src.preprocessing.preprocess import (
    validate_schema,
    check_missing_values,
    check_duplicates,
    validate_timestamp_type,
    check_timestamp_ordering,
)


def test_data_quality():
    df = load_data("data/raw/pump_data.csv")

    assert validate_schema(df) is True
    assert check_missing_values(df).sum() == 0
    assert check_duplicates(df) == 0
    assert validate_timestamp_type(df) is True
    assert check_timestamp_ordering(df) is True