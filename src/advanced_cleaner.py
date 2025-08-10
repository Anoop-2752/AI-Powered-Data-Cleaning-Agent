import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def apply_custom_rules(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Apply user-defined cleaning rules from config.
    Example rules:
      - drop_columns: ["col1", "col2"]
      - replace_values: { "status": {"N/A": "Unknown"} }
      - outlier_limits: { "price": [0, 1000] }
    """
    df = df.copy()

    if "drop_columns" in config:
        for col in config["drop_columns"]:
            if col in df.columns:
                df.drop(columns=col, inplace=True)

    if "replace_values" in config:
        for col, replacements in config["replace_values"].items():
            if col in df.columns:
                df[col] = df[col].replace(replacements)

    if "outlier_limits" in config:
        for col, limits in config["outlier_limits"].items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                low, high = limits
                df[col] = np.clip(df[col], low, high)

    return df


def advanced_imputation(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Advanced missing value imputation using KNN for numeric columns.
    Falls back to median/mode for non-numeric.
    """
    df = df.copy()

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns

    # KNN Imputation for numeric
    if len(numeric_cols) > 0:
        imputer = KNNImputer(n_neighbors=config.get("knn_neighbors", 3))
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    # Fill categorical/text with mode
    for col in non_numeric_cols:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"
            df[col] = df[col].fillna(mode_value)

    return df
