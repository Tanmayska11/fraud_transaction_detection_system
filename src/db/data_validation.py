#src/data_validation.py

import pandas as pd
from src.db.db import get_engine


def validate_data():
    engine = get_engine()

    print("🔍 Running data validation...")

    # NULL CHECK
    nulls = pd.read_sql("""
        SELECT 
            COUNT(*) FILTER (WHERE amount IS NULL) AS null_amount,
            COUNT(*) FILTER (WHERE type IS NULL) AS null_type
        FROM transactions_raw
    """, engine)

    print("NULL CHECK:\n", nulls)

    # DUPLICATES CHECK
    duplicates = pd.read_sql("""
        SELECT COUNT(*) FROM (
            SELECT *, COUNT(*) 
            OVER (PARTITION BY step, amount, nameOrig, nameDest) as cnt
            FROM transactions_raw
        ) t
        WHERE cnt > 1
    """, engine)

    print("DUPLICATES:", duplicates.iloc[0, 0])

    # FRAUD DISTRIBUTION
    fraud_dist = pd.read_sql("""
        SELECT isFraud, COUNT(*) 
        FROM transactions_raw
        GROUP BY isFraud
    """, engine)

    print("FRAUD DISTRIBUTION:\n", fraud_dist)


if __name__ == "__main__":
    validate_data()