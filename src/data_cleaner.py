import pandas as pd
import numpy as np
from src.column_type_detector import detect_column_types

def clean_data(df: pd.DataFrame):
    """
    Adaptive + rule-based cleaning based on detected column types.
    Returns (cleaned_df, issues_list).
    """
    if df is None:
        return None, ["No dataframe provided to clean."]

    issues = []
    df = df.copy()

    # --- Normalize column names ---
    original_cols = list(df.columns)
    df.columns = [c.strip() for c in df.columns]
    if original_cols != list(df.columns):
        issues.append("Stripped whitespace from column names.")

    # --- Drop exact duplicates ---
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    after = df.shape[0]
    removed = before - after
    if removed > 0:
        issues.append(f"Removed {removed} duplicate rows.")

    # --- Detect column types ---
    col_types = detect_column_types(df)
    issues.append(f"Detected column types: {col_types}")

    # --- Apply type-specific cleaning ---
    for col, ctype in col_types.items():
        if ctype == "id":
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.strip()
            continue

        if ctype == "date":
            df[col] = pd.to_datetime(df[col], errors="coerce")
            after_invalid = int(df[col].isna().sum())
            if after_invalid > 0:
                issues.append(f"{col}: {after_invalid} invalid/unparseable entries set to NaT.")

        elif ctype == "numeric":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            missing_before = int(df[col].isna().sum())
            median = df[col].median()
            if pd.notna(median):
                df[col] = df[col].fillna(median)
                filled = missing_before - int(df[col].isna().sum())
                if filled > 0:
                    issues.append(f"{col}: filled {filled} missing/invalid values with median ({median}).")

            if col.lower().startswith("quant"):
                negs = int((df[col] < 0).sum())
                if negs > 0:
                    df.loc[df[col] < 0, col] = df.loc[df[col] < 0, col].abs()
                    issues.append(f"{col}: converted {negs} negative values to positive.")

        elif ctype == "categorical":
            df[col] = df[col].astype(str).str.strip().replace(
                {"nan": pd.NA, "None": pd.NA, "": pd.NA}
            )
            missing_before = int(df[col].isna().sum())
            if missing_before > 0:
                df[col] = df[col].fillna("Unknown")
                issues.append(f"{col}: filled {missing_before} missing values with 'Unknown'.")
            df[col] = df[col].where(df[col].isna(), df[col].str.title())

        elif ctype == "text":
            df[col] = df[col].astype(str).str.strip()
            issues.append(f"{col}: stripped extra whitespace from text values.")

    return df, issues
