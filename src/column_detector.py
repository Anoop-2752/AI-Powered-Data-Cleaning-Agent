import pandas as pd

def detect_column_types(df: pd.DataFrame):
    """
    Detects column types for each column in the DataFrame.
    Returns a dict: {column_name: 'numeric'/'categorical'/'datetime'/'text'}
    """
    column_types = {}

    for col in df.columns:
        # Try datetime detection
        try:
            parsed_dates = pd.to_datetime(df[col], errors='coerce')
            if parsed_dates.notna().sum() / len(df) > 0.8:  # 80%+ parsable
                column_types[col] = "datetime"
                continue
        except Exception:
            pass

        # Numeric detection
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types[col] = "numeric"
        # Categorical detection
        elif df[col].nunique(dropna=True) / len(df) < 0.05:
            column_types[col] = "categorical"
        # Text detection
        elif pd.api.types.is_string_dtype(df[col]):
            column_types[col] = "text"
        else:
            column_types[col] = "unknown"

    return column_types
