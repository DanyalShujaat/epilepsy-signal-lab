"""Exploratory three-stage EEG classifier based on extracted recording features.

This file-level split is for learning and demonstration. It is not patient
independent validation or suitable for clinical use.
"""
import json
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


data = json.loads(Path("data.json").read_text(encoding="utf-8"))
X = [item["features"] for item in data["records"]]
y = [item["stage"] for item in data["records"]]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
labels = ["interictal", "preictal", "ictal"]
print(f"Exploratory held-out accuracy: {accuracy_score(y_test, predictions):.3f}")
print(classification_report(y_test, predictions, labels=labels, zero_division=0))
print("Confusion matrix, rows=true, columns=predicted:")
print(confusion_matrix(y_test, predictions, labels=labels))
print("Caution: file-level split; patient-independent performance is unknown.")
