import numpy as np
import pandas as pd


REQUIRED_TARGET_COLUMNS = ["timestamp", "pump_number", "status"]


def generate_failure_target(
    df: pd.DataFrame,
    horizon_hours: int = 6,
) -> pd.DataFrame:
    """Create future-failure labels for currently running pump readings.

    The input DataFrame must include timestamp, pump_number, and status columns.
    For each RUNNING row, the generated target indicates whether the same pump
    enters a distinct DOWN event within the selected prediction horizon.
    Only RUNNING rows are returned.
    """
    if horizon_hours <= 0:
        raise ValueError("horizon_hours must be positive.")

    missing_columns = [
        column for column in REQUIRED_TARGET_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    target_column = f"failure_within_{horizon_hours}h"
    original_columns = [
        column for column in df.columns
        if column != target_column
    ]

    work_df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(work_df["timestamp"]):
        work_df["timestamp"] = pd.to_datetime(work_df["timestamp"])

    work_df = work_df.sort_values(
        ["pump_number", "timestamp"]
    ).reset_index(drop=True)

    previous_status = work_df.groupby("pump_number")["status"].shift(1)
    downtime_start = (
        (work_df["status"] == "DOWN")
        & (previous_status == "RUNNING")
    )

    downtime_events = work_df.loc[
        downtime_start,
        ["pump_number", "timestamp"],
    ]
    event_times_by_pump = {
        pump_number: group["timestamp"].to_numpy()
        for pump_number, group in downtime_events.groupby("pump_number")
    }

    eligible_df = work_df.loc[
        work_df["status"] == "RUNNING",
        original_columns,
    ].copy()

    next_failure_time = pd.Series(
        pd.NaT,
        index=eligible_df.index,
        dtype="datetime64[ns]",
    )

    for pump_number, group_index in eligible_df.groupby("pump_number").groups.items():
        failure_times = event_times_by_pump.get(pump_number)

        if failure_times is None or len(failure_times) == 0:
            continue

        current_times = eligible_df.loc[group_index, "timestamp"].to_numpy()
        next_failure_positions = np.searchsorted(
            failure_times,
            current_times,
            side="right",
        )

        has_future_failure = next_failure_positions < len(failure_times)
        pump_next_failure_times = np.full(
            len(group_index),
            np.datetime64("NaT"),
            dtype="datetime64[ns]",
        )
        pump_next_failure_times[has_future_failure] = failure_times[
            next_failure_positions[has_future_failure]
        ]

        next_failure_time.loc[group_index] = pd.to_datetime(
            pump_next_failure_times
        )

    hours_until_failure = (
        next_failure_time - eligible_df["timestamp"]
    ).dt.total_seconds() / 3600

    eligible_df[target_column] = (
        hours_until_failure.notna()
        & (hours_until_failure > 0)
        & (hours_until_failure <= horizon_hours)
    ).astype(int)

    return eligible_df[original_columns + [target_column]]
