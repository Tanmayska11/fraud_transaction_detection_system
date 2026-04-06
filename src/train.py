#src.train.py


import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from src.db.db import get_engine
from src.feature_selection import remove_low_variance, select_by_importance
from src.config import MODEL_PATH

TABLE_NAME = "transactions_processed"
FEATURE_PATH = "models/artifacts/features.pkl"


def load_data():
    engine = get_engine()
    print("📥 Loading processed data from DB...")
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
    print(f"Data shape: {df.shape}")
    return df


def train_model():
    df = load_data()
    df.columns = df.columns.str.lower()

    X = df.drop(columns=["isfraud"])
    y = df["isfraud"]

    # Feature selection
    X = remove_low_variance(X)
    X, importances = select_by_importance(X, y)

    print("\n🔝 Top Features:")
    print(importances.head(10))

    # 🔥 SAVE FEATURE LIST (MOST IMPORTANT FIX)
    joblib.dump(X.columns.tolist(), FEATURE_PATH)
    print(f"💾 Features saved at: {FEATURE_PATH}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # -------------------------------
    # Calculate class imbalance BEFORE SMOTE
    # -------------------------------
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)

    # -------------------------------
    # APPLY SMOTE (ONLY ON TRAIN DATA)
    # -------------------------------
    smote = SMOTE(sampling_strategy=0.1, random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    print(f"After SMOTE: {X_train.shape}, Fraud ratio: {sum(y_train)/len(y_train):.4f}")

    # -------------------------------
    # Model
    # -------------------------------
    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,  # ✅ FIXED
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )

    # 🔥 SAVE TEST DATA (IMPORTANT)
    TEST_PATH = "models/artifacts/test_data.pkl"

    joblib.dump((X_test, y_test), TEST_PATH)
    print(f"💾 Test data saved at: {TEST_PATH}")

    print("\n🌲 Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

    print("\n📉 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    print(f"\n💾 Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()