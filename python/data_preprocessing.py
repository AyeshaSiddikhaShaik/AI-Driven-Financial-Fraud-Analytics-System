"""
Data Preprocessing Module

Loads the PaySim dataset,
creates a balanced sample,
and saves it for further analysis.
"""
# ============================================================
# Import Required Libraries
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# Load the Dataset
# ============================================================
import os

print("Current Working Directory:", os.getcwd())
print("Script Location:", os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "synthetic financial dataset.csv")

print("Reading from:", DATA_PATH)

df = pd.read_csv(DATA_PATH)
# ============================================================
# Missing Values
# ============================================================

print(df.isnull().sum())

# Import Sampling Library

from sklearn.model_selection import train_test_split

# Generate Stratified Sample
sample_df, _ = train_test_split(
    df,
    train_size=500000,
    stratify=df["isFraud"],
    random_state=42)

# Verify the Sample Size
print("Original Dataset Shape :", df.shape)
print("Sample Dataset Shape   :", sample_df.shape)

# Compare Fraud Distribution
print("Original Dataset Fraud Distribution (%)")
print(df["isFraud"].value_counts(normalize=True) * 100)

print("\nSample Dataset Fraud Distribution (%)")
print(sample_df["isFraud"].value_counts(normalize=True) * 100)

# Save Sample Dataset
SAMPLE_DIR = os.path.join(BASE_DIR, "data", "sample")
os.makedirs(SAMPLE_DIR, exist_ok=True)

SAMPLE_PATH = os.path.join(SAMPLE_DIR, "paysim_sample_500k.csv")

sample_df.to_csv(SAMPLE_PATH, index=False)

print("Sample dataset saved successfully!")
print("Saved at:", SAMPLE_PATH)


print("Sample dataset saved successfully!")