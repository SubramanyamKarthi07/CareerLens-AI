import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned/job_postings_cleaned.csv")

print("=" * 70)
print("        CLEANED DATASET VERIFICATION REPORT")
print("=" * 70)

print(f"\nDataset Shape : {df.shape}")

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

print("\nLast 5 Records")
print(df.tail())

print("\nVerification Completed Successfully!")