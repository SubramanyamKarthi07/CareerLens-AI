import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/job_postings.csv")

print("=" * 60)
print("CAREERLENS-AI DATA EXPLORATION")
print("=" * 60)

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nFirst 5 Records")
print(df.head())

print("\nStatistical Summary")
print(df.describe(include="all"))