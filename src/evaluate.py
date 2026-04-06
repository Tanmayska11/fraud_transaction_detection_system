#src/evaluate.py

import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from src.config import MODEL_PATH

TEST_PATH = "models/artifacts/test_data.pkl"


def evaluate_model():
    print("📥 Loading test data...")
    X, y = joblib.load(TEST_PATH)

    model = joblib.load(MODEL_PATH)

    print("🔮 Generating predictions...")
    y_prob = model.predict_proba(X)[:, 1]

    thresholds = [0.5, 0.6, 0.7, 0.8]

    best_threshold = 0.8
    final_pred = None

    for t in thresholds:
        print(f"\n===== Threshold: {t} =====")
        y_pred = (y_prob >= t).astype(int)

        print(classification_report(y, y_pred))
        print(confusion_matrix(y, y_pred))

        if t == best_threshold:
            final_pred = y_pred

    # -------------------------------
    # FINAL METRICS (FIXED)
    # -------------------------------
    print("\n📊 Final Model Performance (Threshold = 0.8)")
    print(classification_report(y, final_pred))

    cm = confusion_matrix(y, final_pred)
    print("\n📉 Confusion Matrix:")
    print(cm)

    plt.figure()
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion Matrix")

    plt.savefig("models/artifacts/confusion_matrix.png")
    plt.close()

    auc = roc_auc_score(y, y_prob)
    print(f"\n📈 ROC-AUC Score: {auc:.4f}")

    # -------------------------------
    # FN ANALYSIS
    # -------------------------------
    print("\n🔍 Analyzing missed fraud cases...")

    fn_mask = (y == 1) & (final_pred == 0)
    fn_cases = X[fn_mask].copy()

    print(f"❗ Total missed fraud cases: {fn_cases.shape[0]}")

    if fn_cases.shape[0] > 0:
        print(fn_cases.head())
        print(fn_cases.describe())


if __name__ == "__main__":
    evaluate_model()