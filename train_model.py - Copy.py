"""
Model Training Script for EduPulse AI
Trains a scikit-learn Random Forest Classifier to predict student academic risk level.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

FEATURE_COLS = [
    "attendance_rate",
    "gpa",
    "assignment_completion_rate",
    "midterm_score",
    "study_hours_per_week",
    "lms_engagement_score",
    "participation_score",
    "stress_level"
]

TARGET_COL = "risk_level"

def train_risk_model(data_path="data/students_1200.csv", model_dir="models"):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at '{data_path}'. Please run generate_data.py first.")

    df = pd.read_csv(data_path)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # Stratified split to maintain risk class proportions
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Initialize Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )

    clf.fit(X_train, y_train)

    # Evaluate model
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("=" * 50)
    print("[INFO] EduPulse AI - Model Training Results")
    print("=" * 50)
    print(f"Accuracy Score: {acc:.2%}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(pd.DataFrame(
        confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"]),
        index=["True Low", "True Medium", "True High"],
        columns=["Pred Low", "Pred Medium", "Pred High"]
    ))

    # Compute cohort statistics for normalization & benchmarking in dashboard
    cohort_stats = {
        col: {"mean": float(X[col].mean()), "std": float(X[col].std()), "min": float(X[col].min()), "max": float(X[col].max())}
        for col in FEATURE_COLS
    }

    # Prepare model artifact payload
    artifact = {
        "model": clf,
        "features": FEATURE_COLS,
        "classes": list(clf.classes_),
        "feature_importances": dict(zip(FEATURE_COLS, clf.feature_importances_)),
        "cohort_stats": cohort_stats
    }

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "risk_model.pkl")
    joblib.dump(artifact, model_path)

    # Compute SHA-256 hash for model integrity verification
    import hashlib
    hasher = hashlib.sha256()
    with open(model_path, "rb") as f:
        hasher.update(f.read())
    model_hash = hasher.hexdigest()

    hash_path = model_path + ".sha256"
    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(model_hash)

    print(f"\n[SUCCESS] Model artifact successfully saved to '{model_path}' (SHA-256: {model_hash[:12]}...)")



    return artifact

if __name__ == "__main__":
    train_risk_model()
