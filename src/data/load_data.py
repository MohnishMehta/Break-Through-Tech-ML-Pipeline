import pandas as pd

from src.preprocessing.preprocess import validate_schema


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(
        file_path,
        parse_dates=["timestamp"],
    )


if __name__ == "__main__":
    df = load_data("data/raw/pump_data.csv")
    validate_schema(df)
    print("Data loaded and validated successfully.")