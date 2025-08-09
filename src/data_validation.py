def validate_data(df):
    print("🔍 Validating data...")
    issues = []

    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        issues.append(f"Dataset contains {missing_count} missing values.")

    if "Transaction Date" in df.columns:
        invalid_dates = df[~df["Transaction Date"].astype(str).str.match(r"\d{4}-\d{2}-\d{2}", na=False)]
        if not invalid_dates.empty:
            issues.append("Invalid dates found in 'Transaction Date' column.")

    return issues
