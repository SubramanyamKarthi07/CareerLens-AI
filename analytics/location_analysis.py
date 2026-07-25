import pandas as pd
from pathlib import Path

# -----------------------------
# Load Dataset
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

data_path = BASE_DIR / "data" / "cleaned" / "job_postings_cleaned.csv"

df = pd.read_csv(data_path)

# -----------------------------
# Handle Missing Values
# -----------------------------
df["location"] = df["location"].fillna("Unknown")

# -----------------------------
# Location Analysis
# -----------------------------
location_summary = (
    df.groupby("location")
      .agg(
          Total_Jobs=("id", "count"),
          Companies=("company", "nunique"),
          Unique_Roles=("title", "nunique")
      )
      .sort_values("Total_Jobs", ascending=False)
      .reset_index()
)

# Calculate percentage of total jobs
location_summary["Job_Percentage"] = (
    location_summary["Total_Jobs"] /
    location_summary["Total_Jobs"].sum() * 100
).round(2)

# -----------------------------
# Save Report
# -----------------------------
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "location_analysis.csv"

location_summary.to_csv(output_file, index=False)

# -----------------------------
# Display Results
# -----------------------------
print("=" * 60)
print("LOCATION ANALYTICS REPORT")
print("=" * 60)

print(location_summary.head(10))

print("\nTotal Locations :", location_summary.shape[0])

print(f"\nReport saved successfully to:\n{output_file}")