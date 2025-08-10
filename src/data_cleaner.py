import pandas as pd
import numpy as np
from src.column_type_detector import detect_column_types

def clean_data(df: pd.DataFrame):
    """
    Perform automated cleaning steps and return (cleaned_df, issues_list).
    Issues list contains human-readable descriptions of changes applied.
    """
    if df is None:
        return None, ["No dataframe provided to clean."]

    issues = []
    df = df.copy()

    # Normalize column names (strip)
    original_cols = list(df.columns)
    df.columns = [c.strip() for c in df.columns]
    if original_cols != list(df.columns):
        issues.append("Stripped whitespace from column names.")

    # 1. Drop exact duplicates
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    after = df.shape[0]
    removed = before - after
    if removed > 0:
        issues.append(f"Removed {removed} duplicate rows.")

    # 2. Parse dates (attempt best-effort)
    if 'Transaction Date' in df.columns:
        # Try to coerce to datetime
        parsed = pd.to_datetime(df['Transaction Date'], errors='coerce')
        invalid_before = df['Transaction Date'].isna().sum() if df['Transaction Date'].dtype == object else 0
        df['Transaction Date'] = parsed
        invalid_after = df['Transaction Date'].isna().sum()
        if invalid_after > 0:
            issues.append(f"Transaction Date: {invalid_after} invalid/unparseable entries set to NaT.")

    # 3. Standardize text columns and replace obvious invalid markers
    text_cols = [c for c in df.select_dtypes(include=['object']).columns]
    bad_tokens = {"error", "unknown", "nan", "none", ""}
    for col in text_cols:
        # strip, collapse spaces, title case
        df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
        # normalize case
        df[col] = df[col].replace('nan', '').replace('None', '')
        # Replace common invalid tokens with empty string for further handling
        lowered = df[col].str.lower()
        mask_bad = lowered.isin(bad_tokens)
        if mask_bad.any():
            count_bad = mask_bad.sum()
            df.loc[mask_bad, col] = pd.NA
            issues.append(f"{col}: {count_bad} values marked as invalid and set to missing (NA).")
        # Title case
        df[col] = df[col].where(df[col].isna(), df[col].str.title())

    # 4. Numeric conversions & missing numeric fill
    numeric_candidates = ['Quantity', 'Price Per Unit', 'Total Spent']
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            missing_before = df[col].isna().sum()
            if df[col].dtype.kind in 'fiu':  # numeric
                # Use median imputation for numeric columns
                median = df[col].median()
                if pd.notna(median):
                    df[col] = df[col].fillna(median)
                    missing_after = df[col].isna().sum()
                    filled = missing_before - missing_after
                    if filled > 0:
                        issues.append(f"{col}: filled {filled} missing values with median ({median}).")
            # Fix negatives for quantity
            if col == 'Quantity':
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    df.loc[df[col] < 0, col] = df.loc[df[col] < 0, col].abs()
                    issues.append(f"Quantity: converted {neg_count} negative values to positive.")

    # 5. Final basic cleanup: fill categorical missing with 'Unknown'
    for col in ['Item', 'Payment Method', 'Location']:
        if col in df.columns:
            missing_before = df[col].isna().sum()
            if missing_before > 0:
                df[col] = df[col].fillna("Unknown")
                issues.append(f"{col}: filled {missing_before} missing values with 'Unknown'.")

    return df, issues




def clean_data(df: pd.DataFrame):
    """
    Adaptive cleaning based on detected column types.
    Returns (cleaned_df, issues_list).
    """
    if df is None:
        return None, ["No dataframe provided to clean."]

    issues = []
    df = df.copy()

    # normalize column names
    df.columns = [c.strip() for c in df.columns]

    # detect column types
    col_types = detect_column_types(df)
    issues.append(f"Detected column types: {col_types}")

    # iterate columns and apply cleaning based on type
    for col, ctype in col_types.items():
        if ctype == "id":
            # leave as-is, but strip spaces if string
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.strip()
            continue

        if ctype == "date":
            before_invalid = df[col].isna().sum() if df[col].dtype == object else 0
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
                missing_after = int(df[col].isna().sum())
                filled = missing_before - missing_after
                if filled > 0:
                    issues.append(f"{col}: filled {filled} missing/invalid values with median ({median}).")
            # convert integerlike numeric columns to int if appropriate
            # keep as float to avoid unexpected truncation

            # fix negative quantity if column named like quantity
            if col.lower().startswith("quant"):
                negs = int((df[col] < 0).sum())
                if negs > 0:
                    df.loc[df[col] < 0, col] = df.loc[df[col] < 0, col].abs()
                    issues.append(f"{col}: converted {negs} negative values to positive.")

        elif ctype == "categorical":
            # normalize text
            df[col] = df[col].astype(str).str.strip().replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})
            missing_before = int(df[col].isna().sum())
            if missing_before > 0:
                df[col] = df[col].fillna("Unknown")
                issues.append(f"{col}: filled {missing_before} missing values with 'Unknown'.")
            # title-case values for nicer output (leave IDs/labels untouched)
            df[col] = df[col].where(df[col].isna(), df[col].str.title())

    return df, issues
