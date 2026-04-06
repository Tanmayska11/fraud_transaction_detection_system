#src/preprocessing.py

import pandas as pd


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    print("🧹 Starting preprocessing...")

    # -------------------------------
    # 1. Remove duplicates
    # -------------------------------
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed duplicates: {before - len(df)}")

    # -------------------------------
    # 2. Drop irrelevant columns
    # -------------------------------
    df = df.drop(columns=["nameorig", "namedest"], errors="ignore")

    # -------------------------------
    # 3. Handle missing values
    # -------------------------------
    df = df.dropna()

    # -------------------------------
    # 4. Validate balances
    # Remove rows where balances are negative (invalid cases)
    # -------------------------------
    df = df[
        (df["oldbalanceorg"] >= 0) &
        (df["newbalanceorig"] >= 0) &
        (df["oldbalancedest"] >= 0) &
        (df["newbalancedest"] >= 0)
    ]

    print(f"✅ Final dataset shape after preprocessing: {df.shape}")

    return df