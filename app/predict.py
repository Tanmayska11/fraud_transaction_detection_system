#src/predict.py


import joblib
import pandas as pd
from src.rules import apply_rules
from src.config import MODEL_PATH
from src.feature_engineering import create_features

FEATURE_PATH = "models/artifacts/features.pkl"

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURE_PATH)


def predict(data: dict):

    # -------------------------------
    # 🔥 STEP 1: RULE ENGINE
    # -------------------------------
    rule_result = apply_rules(data)

    if rule_result is not None:
        return rule_result

    # -------------------------------
    # 🔹 STEP 2: ML MODEL
    # -------------------------------
    df = pd.DataFrame([data])

    df = df.drop(columns=["isFraud", "isfraud"], errors="ignore")

    df = create_features(df)
    df.columns = df.columns.str.lower()

    df = df.reindex(columns=features, fill_value=0)

    threshold = 0.8

    probability = model.predict_proba(df)[0][1]
    prediction = int(probability >= threshold)

    return {
        "fraud_prediction": prediction,
        "fraud_probability": float(probability),
        "reason": "ML model"
    }