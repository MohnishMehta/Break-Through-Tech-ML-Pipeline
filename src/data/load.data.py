import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

if __name__ == "__main__":
    df = load_data("data/raw/pump_data.csv")
    print(df.head())
    print(df.shape)