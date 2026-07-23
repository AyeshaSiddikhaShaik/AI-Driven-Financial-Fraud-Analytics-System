"""
Feature Engineering Module

Creates new features for fraud detection
and saves the processed dataset.
"""

import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAMPLE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sample",
    "paysim_sample_500k.csv"
)

sample_df = pd.read_csv(SAMPLE_PATH)

print("Sample dataset loaded successfully!")
print(sample_df.shape)


# ============================================================
# Create Time-Based Features
# ============================================================

# Hour of the day (0–23)
sample_df["hour"] = sample_df["step"] % 24

# Day number
sample_df["day"] = (sample_df["step"] // 24) + 1

# Display sample records
sample_df[["step", "hour", "day"]].head()

# ============================================================
# Create Balance Difference Features
# ============================================================

sample_df["balanceOrigDiff"] = (
    sample_df["oldbalanceOrg"] -
    sample_df["newbalanceOrig"]
)

sample_df["balanceDestDiff"] = (
    sample_df["newbalanceDest"] -
    sample_df["oldbalanceDest"]
)

sample_df[
    [
        "oldbalanceOrg",
        "newbalanceOrig",
        "balanceOrigDiff",
        "oldbalanceDest",
        "newbalanceDest",
        "balanceDestDiff"
    ]
].head()

# ============================================================
# Create Transaction Ratio Feature
# ============================================================

sample_df["amount_to_balance_ratio"] = (
    sample_df["amount"] /
    (sample_df["oldbalanceOrg"] + 1)
)

sample_df[
    [
        "amount",
        "oldbalanceOrg",
        "amount_to_balance_ratio"
    ]
].head()

# ============================================================
# Create High-Value Transaction Indicator
# ============================================================

threshold = sample_df["amount"].quantile(0.95)

sample_df["high_value_transaction"] = (
    sample_df["amount"] >= threshold
).astype(int)

print(f"95th Percentile Threshold: {threshold:,.2f}")

sample_df[
    [
        "amount",
        "high_value_transaction"
    ]
].head()

# ============================================================
# Create Zero Balance Indicators
# ============================================================

sample_df["zero_balance_sender"] = (
    sample_df["oldbalanceOrg"] == 0
).astype(int)

sample_df["zero_balance_receiver"] = (
    sample_df["oldbalanceDest"] == 0
).astype(int)

print(sample_df[
    [
        "oldbalanceOrg",
        "oldbalanceDest",
        "zero_balance_sender",
        "zero_balance_receiver"
    ]
].head())

# ============================================================
# Save Feature-Engineered Dataset
# ============================================================

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "paysim_feature_engineered.csv"
)

sample_df.to_csv(OUTPUT_PATH, index=False)

print("Feature-engineered dataset saved successfully!")
print("Saved at:", OUTPUT_PATH)

print("Feature-engineered dataset saved successfully.")