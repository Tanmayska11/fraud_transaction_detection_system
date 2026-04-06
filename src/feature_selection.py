#src/feaature_selection.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def remove_low_variance(df: pd.DataFrame, threshold=0.01):
    print("🔍 Removing low variance features...")

    numeric_cols = df.select_dtypes(include=["number"]).columns
    variances = df[numeric_cols].var()

    low_var_cols = variances[variances < threshold].index.tolist()

    print(f"Removing {len(low_var_cols)} low variance features")

    df = df.drop(columns=low_var_cols, errors="ignore")

    return df


def select_by_importance(X, y, threshold=0.01):
    print("🌲 Training model for feature importance...")

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )

    model.fit(X, y)

    importances = pd.Series(model.feature_importances_, index=X.columns)

    selected_features = importances[importances > threshold].index.tolist()

    print(f"Selected {len(selected_features)} features out of {X.shape[1]}")

    return X[selected_features], importances.sort_values(ascending=False)