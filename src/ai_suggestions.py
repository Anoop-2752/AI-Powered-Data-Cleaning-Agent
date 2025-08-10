import pandas as pd

def generate_ai_suggestions(df: pd.DataFrame):
    """
    Analyze the cleaned dataset and return AI-powered suggestions
    for further improvement.
    (Currently rule-based, but can be upgraded to LLM-powered.)
    """
    suggestions = []

    # 1. Check for high missing value columns
    missing_cols = df.isnull().mean() * 100
    high_missing = missing_cols[missing_cols > 20]  # >20% missing
    for col, pct in high_missing.items():
        suggestions.append(
            f"Column '{col}' has {pct:.1f}% missing values. Consider dropping or imputing."
        )

    # 2. Check numeric outliers (very high or low compared to IQR)
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        if not outliers.empty:
            suggestions.append(
                f"Column '{col}' has {len(outliers)} potential outliers."
            )

    # 3. Check for categorical standardization
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        unique_vals = df[col].dropna().nunique()
        if unique_vals < 15:  # small category set
            inconsistent = [
                v for v in df[col].dropna().unique()
                if str(v).strip() != str(v)
            ]
            if inconsistent:
                suggestions.append(
                    f"Column '{col}' may have inconsistent spacing in categories."
                )

    if not suggestions:
        suggestions.append("No additional suggestions. Data looks good!")

    return suggestions
