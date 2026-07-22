import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/job_postings.csv")

print("=" * 70)
print("          CAREERLENS-AI DATASET VERIFICATION REPORT")
print("=" * 70)

# Dataset Size
print("\n1. Dataset Size")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# Column Names
print("\n2. Column Names")
for i, col in enumerate(df.columns, start=1):
    print(f"{i}. {col}")

# Data Types
print("\n3. Data Types")
print(df.dtypes)

# Missing Values
print("\n4. Missing Values")
missing = df.isnull().sum()
print(missing)

# Missing Value Percentage
print("\n5. Missing Value Percentage")
missing_percent = (missing / len(df)) * 100
print(missing_percent.round(2))

# Duplicate Records
print("\n6. Duplicate Records")
print(df.duplicated().sum())

# Unique Values
print("\n7. Unique Values per Column")
print(df.nunique())

# Memory Usage
print("\n8. Memory Usage")
print(df.memory_usage(deep=True))

# Statistical Summary
print("\n9. Statistical Summary")
print(df.describe(include="all"))

# Sample Records
print("\n10. First Five Records")
print(df.head())

print("\n11. Last Five Records")
print(df.tail())

print("\n" + "=" * 70)
print("Dataset Verification Completed Successfully")
print("=" * 70)