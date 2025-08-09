import pandas as pd

def clean_data(df):
    print("✨ Cleaning data...")
    df = df.drop_duplicates()
    df.columns = [col.strip() for col in df.columns]
    print(f"✨ Data cleaned! Shape: {df.shape}")
    print(df.head(3), "\n")
    return df
