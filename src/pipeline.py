#src/pipeline.py


import pandas as pd
import io
from sqlalchemy import text

from src.db.db import get_engine
from src.preprocessing import preprocess_data
from src.feature_engineering import create_features


RAW_TABLE = "transactions_raw"
PROCESSED_TABLE = "transactions_processed"


# =====================================================
# ⚡ FAST INSERT USING POSTGRES COPY
# =====================================================
def fast_insert(df, engine, table_name: str):
    print("⚡ Using PostgreSQL COPY for fast insertion...")

    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()

        cursor.copy_expert(
            f"COPY {table_name} FROM STDIN WITH CSV",
            buffer
        )

        conn.commit()
        cursor.close()

    finally:
        conn.close()

    print("✅ Fast insert completed!")


# =====================================================
# 🔄 MAIN PIPELINE
# =====================================================
def run_pipeline():
    engine = get_engine()

    # -------------------------------
    # Load data from DB
    # -------------------------------
    print("📥 Loading raw data from DB...")
    df = pd.read_sql(f"SELECT * FROM {RAW_TABLE}", engine)
    print(f"Raw shape: {df.shape}")

    # -------------------------------
    # Preprocessing
    # -------------------------------
    df_clean = preprocess_data(df)

    # -------------------------------
    # Feature Engineering
    # -------------------------------
    df_features = create_features(df_clean)

    # 🔥 Enforce lowercase (CRITICAL)
    df_features.columns = df_features.columns.str.lower()

    print(f"Final feature shape: {df_features.shape}")

    # -------------------------------
    # Safety checks (VERY IMPORTANT)
    # -------------------------------
    assert "isfraud" in df_features.columns, "Target column missing!"

    # -------------------------------
    # Save to PostgreSQL
    # -------------------------------
    print("💾 Saving processed data to DB...")

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {PROCESSED_TABLE}"))

    # Create schema
    df_features.head(0).to_sql(
        name=PROCESSED_TABLE,
        con=engine,
        index=False
    )

    # Fast insert
    fast_insert(df_features, engine, PROCESSED_TABLE)

    print("🎯 Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()