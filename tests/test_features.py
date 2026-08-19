import pandas as pd

from predictive_maintenance.features.build_features import generate_failure_target


def make_pump_rows(rows):
    return pd.DataFrame(
        rows,
        columns=["pump_number", "timestamp", "status"],
    )


def labels_by_timestamp(labeled_df, target_column="failure_within_6h"):
    return dict(
        zip(
            labeled_df["timestamp"].dt.strftime("%H:%M"),
            labeled_df[target_column],
        )
    )


def test_positive_label_within_six_hours():
    df = make_pump_rows(
        [
            (1, "2026-01-01 08:00", "RUNNING"),
            (1, "2026-01-01 09:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    labels = labels_by_timestamp(labeled_df)
    assert labels["08:00"] == 1
    assert labels["09:00"] == 1


def test_negative_label_outside_six_hours():
    df = make_pump_rows(
        [
            (1, "2026-01-01 01:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    labels = labels_by_timestamp(labeled_df)
    assert labels["01:00"] == 0


def test_down_rows_are_excluded():
    df = make_pump_rows(
        [
            (1, "2026-01-01 08:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    assert set(labeled_df["status"]) == {"RUNNING"}


def test_consecutive_down_rows_count_as_one_event_start():
    df = make_pump_rows(
        [
            (1, "2026-01-01 01:00", "RUNNING"),
            (1, "2026-01-01 04:00", "DOWN"),
            (1, "2026-01-01 05:00", "DOWN"),
            (1, "2026-01-01 06:00", "DOWN"),
            (1, "2026-01-01 07:00", "RUNNING"),
        ]
    )

    labeled_df = generate_failure_target(df)

    labels = labels_by_timestamp(labeled_df)
    assert labels["01:00"] == 1
    assert labels["07:00"] == 0


def test_multiple_pumps_are_labeled_independently():
    df = make_pump_rows(
        [
            (1, "2026-01-01 01:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
            (2, "2026-01-01 01:00", "RUNNING"),
            (2, "2026-01-01 05:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    pump_1_label = labeled_df.loc[
        labeled_df["pump_number"] == 1,
        "failure_within_6h",
    ].iloc[0]
    pump_2_label = labeled_df.loc[
        labeled_df["pump_number"] == 2,
        "failure_within_6h",
    ].iloc[0]

    assert pump_1_label == 0
    assert pump_2_label == 1


def test_no_future_failure_receives_negative_label():
    df = make_pump_rows(
        [
            (1, "2026-01-01 08:00", "RUNNING"),
            (1, "2026-01-01 09:00", "RUNNING"),
        ]
    )

    labeled_df = generate_failure_target(df)

    assert labeled_df["failure_within_6h"].tolist() == [0, 0]


def test_exact_six_hour_boundary_is_positive():
    df = make_pump_rows(
        [
            (1, "2026-01-01 06:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    assert labeled_df["failure_within_6h"].iloc[0] == 1


def test_just_outside_six_hour_boundary_is_negative():
    df = make_pump_rows(
        [
            (1, "2026-01-01 05:59", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df)

    assert labeled_df["failure_within_6h"].iloc[0] == 0


def test_input_dataframe_is_not_mutated():
    df = make_pump_rows(
        [
            (1, "2026-01-01 08:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )
    original_df = df.copy(deep=True)

    generate_failure_target(df)

    pd.testing.assert_frame_equal(df, original_df)


def test_dynamic_horizon_support():
    df = make_pump_rows(
        [
            (1, "2026-01-01 08:00", "RUNNING"),
            (1, "2026-01-01 10:00", "RUNNING"),
            (1, "2026-01-01 12:00", "DOWN"),
        ]
    )

    labeled_df = generate_failure_target(df, horizon_hours=3)

    labels = labels_by_timestamp(labeled_df, target_column="failure_within_3h")
    assert "failure_within_3h" in labeled_df.columns
    assert labels["08:00"] == 0
    assert labels["10:00"] == 1
