# Import Required Libraries
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)

from sklearn.ensemble import (
    RandomForestClassifier,
    IsolationForest
)

import joblib

# Load Feature-Engineered Dataset
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "paysim_feature_engineered.csv"
)

print("Reading from:", PROCESSED_PATH)

df = pd.read_csv(PROCESSED_PATH)
print(df.columns.tolist())
df.head()

# Remove Non-Predictive Features
df.drop(
    columns=["nameOrig", "nameDest"],
    inplace=True
)

df.head()

# Encode Categorical Variables
encoder = LabelEncoder()

df["type"] = encoder.fit_transform(df["type"])

df.head()

# Feature Selection
features = [
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "balanceOrigDiff",
    "balanceDestDiff",
    "amount_to_balance_ratio",
    "high_value_transaction",
    "zero_balance_sender",
    "zero_balance_receiver"
]

X = df[features]


X = df[features]

y = df["isFraud"]

print(X.shape)
print(y.shape)

# Train-Test Split
# ============================================================
# Train-Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Features :", X_train.shape)
print("Testing Features  :", X_test.shape)
print("Training Labels   :", y_train.shape)
print("Testing Labels    :", y_test.shape)

# Verify Class Distribution
# ============================================================
# Verify Class Distribution
# ============================================================

print("Training Set")
print(y_train.value_counts())

print("\nTesting Set")
print(y_test.value_counts())

# Train Random Forest Classifier
# ============================================================
# Train Random Forest
# ============================================================

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

print("Random Forest Model Trained Successfully.")

# Save the trained model


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "fraud_detection_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

# Save model
joblib.dump(rf_model, MODEL_PATH)

# Save label encoder
joblib.dump(encoder, ENCODER_PATH)

print("Model saved successfully!")
print("Saved at:", MODEL_PATH)

print("Encoder saved successfully!")
print("Saved at:", ENCODER_PATH)
