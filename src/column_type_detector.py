import pandas as pd
import numpy as np
import warnings

def detect_column_types(df: pd.DataFrame) -> dict:
    """
    Automatically detect column types:
    - id: Unique identifiers
    - date: Date or datetime values (with format detection)
    - numeric: Integers or floats
    - categorical: Strings or limited categories
    """
    warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
    col_types = {}

    def detect_date_format(sample_series):
        """
        Guess common date format from a sample of values.
        Returns format string if detected, else None.
        """
        sample_values = sample_series.dropna().astype(str).head(10)
        formats = [
            "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
            "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"
        ]
        for fmt in formats:
            try:
                pd.to_datetime(sample_values, format=fmt, errors="raise")
                return fmt
            except Exception:
                continue
        return None

    for col in df.columns:
        series = df[col]

        # 1️⃣ ID detection — all values unique
        if series.nunique(dropna=True) == len(series):
            col_types[col] = "id"
            continue

        # 2️⃣ Numeric detection FIRST (prevents big numbers from being parsed as dates)
        if pd.api.types.is_numeric_dtype(series):
            col_types[col] = "numeric"
            continue
        try:
            numeric = pd.to_numeric(series, errors="coerce")
            if numeric.notna().mean() > 0.8:
                col_types[col] = "numeric"
                continue
        except Exception:
            pass

        # 3️⃣ Date detection
        date_fmt = detect_date_format(series)
        if date_fmt:
            parsed = pd.to_datetime(series, format=date_fmt, errors="coerce")
            if parsed.notna().mean() > 0.8:
                years = parsed.dt.year.dropna()
                if (years.between(1900, 2100).mean() > 0.8):
                    col_types[col] = "date"
                    continue
        else:
            # Generic parsing only if column *looks* like a date
            if series.astype(str).str.contains(r"\d{4}|\d{2}[-/]\d{2}[-/]\d{2}").mean() > 0.8:
                parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
                if parsed.notna().mean() > 0.8:
                    years = parsed.dt.year.dropna()
                    if (years.between(1900, 2100).mean() > 0.8):
                        col_types[col] = "date"
                        continue

        # 4️⃣ Default categorical
        col_types[col] = "categorical"

    return col_types
