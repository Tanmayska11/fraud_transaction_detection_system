

#src/feature_engineering.py

import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    print("⚙️ Starting feature engineering...")

    df.columns = df.columns.str.lower()

    # =====================================================
    # 🔹 1. BALANCE FEATURES
    # =====================================================

    df["orig_balance_error"] = (
        df["oldbalanceorg"] - df["amount"] - df["newbalanceorig"]
    )

    df["dest_balance_error"] = (
        df["oldbalancedest"] + df["amount"] - df["newbalancedest"]
    )

    df["orig_amount_ratio"] = df["amount"] / (df["oldbalanceorg"] + 1)
    df["dest_amount_ratio"] = df["amount"] / (df["oldbalancedest"] + 1)

    # =====================================================
    # 🔹 2. BEHAVIORAL FEATURES
    # =====================================================

    df["is_orig_empty"] = (df["oldbalanceorg"] == 0).astype(int)
    df["is_dest_empty"] = (df["oldbalancedest"] == 0).astype(int)

    df["is_full_drain"] = (
        (df["amount"] == df["oldbalanceorg"]) &
        (df["newbalanceorig"] == 0)
    ).astype(int)

    df["is_high_amount"] = (df["amount"] > df["amount"].quantile(0.95)).astype(int)

    # =====================================================
    # 🔥 3. NEW CRITICAL FEATURES (BASED ON FN ANALYSIS)
    # =====================================================

    # 🚨 Fraud pattern: money sent from empty account
    df["empty_orig_with_amount"] = (
        (df["oldbalanceorg"] == 0) & (df["amount"] > 0)
    ).astype(int)

    # 🚨 Amount when balance is zero (strong signal)
    df["amount_when_orig_empty"] = df["amount"] * df["is_orig_empty"]

    # 🚨 New balance remains zero after transaction
    df["zero_balance_after_txn"] = (df["newbalanceorig"] == 0).astype(int)

    # 🚨 Combined strong fraud signal
    df["suspicious_zero_pattern"] = (
        (df["oldbalanceorg"] == 0) &
        (df["newbalanceorig"] == 0) &
        (df["amount"] > 0)
    ).astype(int)

    # =====================================================
    # 🔹 4. TRANSACTION FEATURES
    # =====================================================

    # ✅ FIX: keep ALL categories (NO drop_first)
    type_categories = ["CASH_OUT", "PAYMENT", "TRANSFER", "DEBIT", "CASH_IN"]

    df["type"] = pd.Categorical(df["type"], categories=type_categories)

    df = pd.get_dummies(df, columns=["type"], drop_first=False)
    # =====================================================
    # 🔹 5. TIME FEATURES
    # =====================================================

    df["hour"] = df["step"] % 24
    df["is_night"] = df["hour"].isin([0,1,2,3,4]).astype(int)

    # =====================================================
    # 🔹 6. CLEANUP
    # =====================================================

    df = df.drop(columns=["step"], errors="ignore")

    print(f"✅ Feature engineering completed. Shape: {df.shape}")

    return df