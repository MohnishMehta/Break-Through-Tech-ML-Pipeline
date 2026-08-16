import pandas as pd

EXPECTED_COLUMNS = [
    "timestamp",
    "pump_throughput_m3ph",
    "operating_pressure_bar",
    "vibration_mm_s",
    "bearing_temp_C",
    "status",
    "pump_number",
]

def validate_schema(df):
    missing_columns = [
        column for column in EXPECTED_COLUMNS 
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in the DataFrame: {missing_columns}"
        )
    return True

def check_missing_values(df):
    return df.isnull().sum()

def check_duplicates(df):
    return df.duplicated().sum()

def validate_timestamp_type(df):
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        raise TypeError("The 'timestamp' column must be of datetime type.")
    return True

def check_timestamp_ordering(df):
    sorted_df = df.sort_values(["pump_number", "timestamp"])

    return df[["pump_number", "timestamp"]].reset_index(drop=True).equals(
        sorted_df[["pump_number", "timestamp"]].reset_index(drop=True)
    )
