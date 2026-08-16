# Predictive Maintenance ML Pipeline

An end-to-end machine learning project for industrial pump predictive maintenance. The goal is to use historical pump sensor data to build a system that can eventually identify whether a currently operating pump is at risk of transitioning to a `DOWN` state in the near future.

The project is being rebuilt from the ground up as a production-style ML pipeline, including data validation, preprocessing, feature engineering, model training, experiment tracking, API-based inference, simulated sensor streaming, monitoring, testing, and deployment.

## Project Structure

```text
Break-Through-Tech-ML-Pipeline/
│
├── data/
│   ├── raw/
│   │   └── pump_data.csv
│   └── processed/
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   └── predictive_maintenance/
│       ├── __init__.py
│       ├── api/
│       ├── data/
│       ├── features/
│       ├── models/
│       └── preprocessing/
│
├── tests/
│
├── models/
│
├── .gitignore
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Dataset Overview

The project uses historical sensor readings collected from industrial pumps.

### Dataset Characteristics

* **Rows:** 720,050
* **Columns:** 7
* **Number of pumps:** 50
* **Sampling interval:** 10 minutes
* **Time range:** April 15, 2025 to July 24, 2025

### Dataset Columns

| Column                   | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| `timestamp`              | Time the sensor reading was recorded                 |
| `pump_throughput_m3ph`   | Pump throughput in cubic meters per hour             |
| `operating_pressure_bar` | Pump operating pressure in bar                       |
| `vibration_mm_s`         | Pump vibration measurement in millimeters per second |
| `bearing_temp_C`         | Bearing temperature in degrees Celsius               |
| `status`                 | Current pump state (`RUNNING` or `DOWN`)             |
| `pump_number`            | Identifier for the individual pump                   |

## Data Quality

Initial data validation confirmed:

* No missing values
* No duplicate rows
* All required columns are present
* Sensor columns contain the expected data types
* `timestamp` is parsed as a datetime value
* Readings are ordered by `pump_number` and `timestamp`

These checks are implemented as reusable validation logic in the project rather than relying only on manual inspection.

## Status Distribution

The pump status variable is imbalanced.

Approximately:

* **RUNNING:** 93.3%
* **DOWN:** 6.7%

Because of this imbalance, model performance will not be evaluated using accuracy alone.

Later model evaluation will focus on metrics such as:

* Precision
* Recall
* F1 score
* ROC-AUC
* PR-AUC
* Confusion matrix

Recall will be especially important because failing to detect an upcoming pump failure may be more costly than generating a false warning.

## Predictive Maintenance Objective

The long-term goal is not simply to classify whether a pump is currently `RUNNING` or `DOWN`.

Doing so could create a weak machine learning problem because some sensor values, such as pump throughput, may already directly indicate that a pump is currently down.

Instead, the project will be framed as a predictive maintenance problem:

> Predict whether a currently operating pump is likely to transition to a `DOWN` state within a future prediction window using its current and recent historical sensor behavior.

The exact prediction horizon will be determined during feature engineering after analyzing sensor behavior leading up to downtime events.

Potential prediction windows may include:

* Failure within 1 hour
* Failure within 3 hours
* Failure within 6 hours
* Failure within 12 hours

The selected horizon should provide enough advance warning to make the prediction operationally useful while still preserving meaningful predictive signal.

## Planned ML Pipeline

```text
Historical Pump Data
        ↓
Data Validation
        ↓
Exploratory Data Analysis
        ↓
Target Generation
        ↓
Feature Engineering
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Experiment Tracking
        ↓
Production Model
        ↓
FastAPI Inference Service
        ↓
Simulated Sensor Stream
        ↓
Prediction Storage
        ↓
Monitoring / Drift Detection
```

## Current Project Setup

The project uses a Python virtual environment to isolate dependencies.

Create the environment:

```bash
python3 -m venv .venv
```

Activate it on macOS:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the local project package in editable mode:

```bash
python -m pip install -e .
```

Editable installation allows project modules to be imported consistently from notebooks, tests, scripts, and future API code.

Example:

```python
from predictive_maintenance.data.load_data import load_data
```

## Running Tests

Tests are written using `pytest`.

Run the full test suite from the project root:

```bash
python -m pytest
```

Current tests validate:

* Dataset schema
* Missing values
* Duplicate rows
* Timestamp data type
* Timestamp ordering

## Development Roadmap

The project will be developed incrementally through the following major phases:

1. Project setup and data foundation
2. Data exploration and preprocessing
3. Predictive target design
4. Feature engineering
5. Model training and evaluation
6. MLflow experiment tracking
7. Model packaging and versioning
8. FastAPI prediction service
9. Simulated real-time sensor ingestion
10. PostgreSQL prediction storage
11. Model and data monitoring
12. Docker containerization
13. Automated testing and GitHub Actions
14. Deployment and final documentation

## Technology Stack

Current and planned technologies include:

* Python
* Pandas
* Matplotlib
* Scikit-learn
* Pytest
* MLflow
* FastAPI
* PostgreSQL
* Docker
* GitHub Actions

Additional technologies may be introduced as the production pipeline evolves.
