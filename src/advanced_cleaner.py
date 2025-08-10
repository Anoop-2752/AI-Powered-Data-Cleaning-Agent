import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from .column_detector import detect_column_types

def apply_custom_rules(df, config):
    # Date range filtering
    if "date_columns" in config:
        for col, rules in config["date_columns"].items():
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if "min" in rules:
                    df.loc[df[col] < pd.to_datetime(rules["min"]), col] = pd.NaT
                if "max" in rules:
                    df.loc[df[col] > pd.to_datetime(rules["max"]), col] = pd.NaT

    # Outlier handling
    if "outlier_rules" in config:
        for col, rules in config["outlier_rules"].items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                if rules["method"] == "zscore":
                    z_scores = (df[col] - df[col].mean()) / df[col].std()
                    df.loc[abs(z_scores) > rules["threshold"], col] = np.nan
                elif rules["method"] == "iqr":
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - rules["multiplier"] * IQR
                    upper_bound = Q3 + rules["multiplier"] * IQR
                    df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = np.nan
    return df

def advanced_imputation(df, config):
    col_types = detect_column_types(df)

    # Numeric imputation
    numeric_cols = [c for c, t in col_types.items() if t == "numeric"]
    if numeric_cols and config.get("imputation", {}).get("numeric") == "knn":
        imputer = KNNImputer(n_neighbors=5)
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    elif numeric_cols:
        method = config.get("imputation", {}).get("numeric", "median")
        for col in numeric_cols:
            if method == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif method == "mean":
                df[col].fillna(df[col].mean(), inplace=True)

    # Categorical imputation
    cat_cols = [c for c, t in col_types.items() if t == "categorical"]
    for col in cat_cols:
        method = config.get("imputation", {}).get("categorical", "most_frequent")
        if method == "most_frequent":
            df[col].fillna(df[col].mode()[0], inplace=True)

    return df
