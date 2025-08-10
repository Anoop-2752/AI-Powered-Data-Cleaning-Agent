import pandas as pd
import re

def _looks_like_date(series):
    # quick attempts: if pandas can parse most non-empty items -> date
    sample = series.dropna().astype(str).head(100)
    if sample.empty:
        return False
    try:
        parsed = pd.to_datetime(sample, errors='coerce')
        frac_parsed = parsed.notna().sum() / len(sample)
        return frac_parsed >= 0.6
    except Exception:
        return False

def _looks_like_numeric(series):
    sample = series.dropna().astype(str).head(100)
    if sample.empty:
        return False
    numeric_count = sample.apply(lambda x: re.fullmatch(r"-?\d+(\.\d+)?", x.strip()) is not None).sum()
    return (numeric_count / len(sample)) >= 0.6

def detect_column_types(df):
    """
    Detects column types using heuristics.
    Returns dict: column -> type in {'id','date','numeric','categorical'}
    """
    col_types = {}
    n = len(df)
    for col in df.columns:
        series = df[col]
        # ID heuristic: very high uniqueness and values are strings with letters or mixed
        unique_frac = df[col].nunique(dropna=True) / max(1, n)
        if unique_frac > 0.9:
            # if mostly alphanumeric strings -> id
            sampled = series.dropna().astype(str).head(50)
            if sampled.str.contains(r"[A-Za-z]").any():
                col_types[col] = "id"
                continue

        # Date heuristic
        if _looks_like_date(series):
            col_types[col] = "date"
            continue

        # Numeric heuristic
        if _looks_like_numeric(series):
            col_types[col] = "numeric"
            continue

        # default to categorical
        col_types[col] = "categorical"

    return col_types
