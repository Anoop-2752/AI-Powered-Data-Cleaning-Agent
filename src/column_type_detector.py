import pandas as pd
import numpy as np

def detect_column_types(df: pd.DataFrame) -> dict:
    """
    Automatically detect column types: id, date, numeric, categorical.
    Returns a dict {column_name: type}.
    """
    col_types = {}

    for col in df.columns:
        series = df[col]

        # 1️⃣ ID detection — high uniqueness and mostly non-null
        if series.nunique(dropna=True) == len(series):
            col_types[col] = "id"
            continue

        # 2️⃣ Date detection
        try:
            parsed = pd.to_datetime(series, errors="coerce")
            # If >80% of values successfully parse to datetime, mark as date
            if parsed.notna().mean() > 0.8:
                col_types[col] = "date"
                continue
        except Exception:
            pass

        # 3️⃣ Numeric detection
        if pd.api.types.is_numeric_dtype(series):
            col_types[col] = "numeric"
            continue
        try:
            # Try coercing to numeric
            numeric = pd.to_numeric(series, errors="coerce")
            if numeric.notna().mean() > 0.8:
                col_types[col] = "numeric"
                continue
        except Exception:
            pass

        # 4️⃣ Default to categorical
        col_types[col] = "categorical"

    return col_types
