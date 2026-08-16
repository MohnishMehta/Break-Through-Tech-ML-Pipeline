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