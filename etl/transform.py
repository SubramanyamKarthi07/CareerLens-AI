import pandas as pd

# ----------------------------
# Load Dataset
# ----------------------------
print("=" * 60)
print("CAREERLENS-AI DATA TRANSFORMATION")
print("=" * 60)

df = pd.read_csv("data/raw/job_postings.csv")

print(f"\nOriginal Shape : {df.shape}")

# ----------------------------
# Remove Empty Columns
# ----------------------------
columns_to_drop = ["work_type", "employment_type"]

df.drop(columns=columns_to_drop, inplace=True)

print("\n✓ Removed empty columns")

# ----------------------------
# Fill Missing Values
# ----------------------------
df["company"] = df["company"].fillna("Unknown Company")
df["location"] = df["location"].fillna("Unknown Location")
df["source"] = df["source"].fillna("Unknown")
df["description"] = df["description"].fillna("No Description")

print("✓ Filled missing values")

# ----------------------------
# Convert Date
# ----------------------------
df["date_posted"] = pd.to_datetime(
    df["date_posted"],
    errors="coerce"
)

# Remove rows where date is missing
before = len(df)

df = df.dropna(subset=["date_posted"])

after = len(df)

print(f"✓ Removed {before-after} rows with invalid dates")

# ----------------------------
# Remove Duplicate Records
# ----------------------------
duplicates = df.duplicated().sum()

df = df.drop_duplicates()

print(f"✓ Removed {duplicates} duplicate rows")

# ----------------------------
# Reset Index
# ----------------------------
df.reset_index(drop=True, inplace=True)

# ----------------------------
# Save Clean Dataset
# ----------------------------
output_path = "data/cleaned/job_postings_cleaned.csv"

df.to_csv(output_path, index=False)

print("\nTransformation Completed Successfully!")

print(f"\nFinal Shape : {df.shape}")

print(f"\nClean dataset saved to:\n{output_path}")