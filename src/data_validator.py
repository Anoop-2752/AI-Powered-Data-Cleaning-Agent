import pandas as pd

def validate_data(df):
    """
    Run validations and return a list of issues (empty list if none).
    """
    issues = []
    if df is None:
        return ["No dataframe provided to validate."]

    # 1. Missing values total
    missing_total = int(df.isnull().sum().sum())
    if missing_total > 0:
        issues.append(f"Dataset contains {missing_total} missing values total.")

    # 2. Duplicates check
    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        issues.append(f"Dataset contains {dup_count} duplicate rows.")

    # 3. Transaction Date sanity (if exists)
    if 'Transaction Date' in df.columns:
        # Count NaT
        nat_count = int(df['Transaction Date'].isna().sum())
        if nat_count > 0:
            issues.append(f"Transaction Date contains {nat_count} NaT (invalid/missing dates).")

    # 4. Numeric sanity
    for col in ['Quantity', 'Price Per Unit', 'Total Spent']:
        if col in df.columns:
            # non-numeric or negative checks
            if not pd.api.types.is_numeric_dtype(df[col]):
                issues.append(f"{col} is not numeric.")
            else:
                negs = int((df[col] < 0).sum())
                if negs > 0:
                    issues.append(f"{col} contains {negs} negative values.")

    return issues
