import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data from the given file path.
    Raises FileNotFoundError if file missing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    print(f"\n📂 Loading raw data from: {file_path}")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"📂 Raw data loaded successfully! Shape: {df.shape}")
    print(df.head(3), "\n")
    return df
