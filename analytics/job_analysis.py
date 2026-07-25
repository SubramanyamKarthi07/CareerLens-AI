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
df["title"] = df["title"].fillna("Unknown")

# -----------------------------
# Job Title Analysis
# -----------------------------
job_summary = (
    df.groupby("title")
      .agg(
          Total_Jobs=("id", "count"),
          Companies=("company", "nunique"),
          Locations=("location", "nunique")
      )
      .sort_values("Total_Jobs", ascending=False)
      .reset_index()
)

job_summary["Job_Percentage"] = (
    job_summary["Total_Jobs"] /
    job_summary["Total_Jobs"].sum() * 100
).round(2)

# -----------------------------
# Save Report
# -----------------------------
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "job_analysis.csv"

job_summary.to_csv(output_file, index=False)

# -----------------------------
# Display Results
# -----------------------------
print("=" * 60)
print("JOB TITLE ANALYTICS REPORT")
print("=" * 60)

print(job_summary.head(10))

print("\nTotal Unique Job Titles:", job_summary.shape[0])

print(f"\nReport saved successfully to:\n{output_file}")