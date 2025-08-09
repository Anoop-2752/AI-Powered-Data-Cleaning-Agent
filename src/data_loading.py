import pandas as pd
from src.utils import RAW_DATA_PATH

def load_raw_data():
    print(f"\n📂 Loading raw data from: {RAW_DATA_PATH}")
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"📂 Raw data loaded successfully! Shape: {df.shape}")
        print(df.head(3), "\n")
        return df
    except FileNotFoundError:
        print(f"❌ File not found at {RAW_DATA_PATH}")
        return None
