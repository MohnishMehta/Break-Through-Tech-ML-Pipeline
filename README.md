## Predictive Maintenance Target

The final predictive-maintenance target is:

> Predict whether a pump that is currently `RUNNING` will transition to `DOWN` within the next 6 hours.

The generated target column is:

`failure_within_6h`

### Target Definition

- `1` — the pump is currently `RUNNING` and a distinct downtime event begins within the next 6 hours.
- `0` — the pump is currently `RUNNING` and no distinct downtime event begins within the next 6 hours.

Rows where the pump is already `DOWN` are excluded from the modeling dataset because the objective is to predict future downtime rather than identify a failure that has already occurred.

### Why a 6-Hour Horizon?

Candidate prediction horizons of 1, 3, 6, and 12 hours were compared.

A 6-hour horizon was selected because it provides a practical balance between advance warning and observable pre-failure sensor behavior.

Exploratory analysis showed that during the hours leading up to downtime:

- Vibration increases
- Bearing temperature increases
- Operating pressure decreases modestly
- Pump throughput remains relatively stable

The 6-hour horizon produces approximately:

- 18,000 positive observations
- 671,600 eligible `RUNNING` observations
- 2.68% positive target rate

The target is intentionally imbalanced because downtime events are rare relative to normal pump operation.

### Target Generation

Reusable target-generation logic is implemented in:

`src/predictive_maintenance/features/build_features.py`

The function:

`generate_failure_target(df, horizon_hours=6)`

performs the following steps:

1. Validates the required input columns.
2. Orders readings by pump and timestamp.
3. Detects distinct `RUNNING → DOWN` transitions.
4. Finds the next downtime event for each currently running observation.
5. Calculates the time remaining until that event.
6. Creates the binary future-failure target.
7. Excludes rows where the pump is already `DOWN`.

The function also supports alternative prediction horizons, such as 3 hours or 12 hours, while 6 hours is the selected target for the current model.
