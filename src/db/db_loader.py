import pandas as pd
from src.db.db import get_engine

TABLE_NAME = "public.transactions_raw"

def load_data():
    engine = get_engine()

    print("📥 Loading data from PostgreSQL...")

    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, engine)

    print(f"✅ Loaded data shape: {df.shape}")

    return df