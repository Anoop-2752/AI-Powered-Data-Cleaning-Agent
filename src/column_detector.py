import pandas as pd

def detect_column_types(df):
    column_types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            column_types[col] = "date"
        elif pd.api.types.is_string_dtype(df[col]):
            # Heuristic: low unique count = categorical
            if df[col].nunique(dropna=True) < 50:
                column_types[col] = "categorical"
            else:
                column_types[col] = "text"
        else:
            column_types[col] = "unknown"
    return column_types
