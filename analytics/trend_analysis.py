import pandas as pd
from pathlib import Path

# -----------------------------
# Load Dataset
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

data_path = BASE_DIR / "data" / "cleaned" / "job_postings_cleaned.csv"

df = pd.read_csv(data_path)

# -----------------------------
# Convert Date
# -----------------------------
df["date_posted"] = pd.to_datetime(
    df["date_posted"],
    errors="coerce"
)

# Remove invalid dates
df = df.dropna(subset=["date_posted"])

# Create Month-Year column
df["Month"] = df["date_posted"].dt.to_period("M").astype(str)

# -----------------------------
# Monthly Trend Analysis
# -----------------------------
trend_summary = (
    df.groupby("Month")
      .agg(
          Total_Jobs=("id", "count"),
          Companies=("company", "nunique"),
          Locations=("location", "nunique")
      )
      .sort_index()
      .reset_index()
)

trend_summary["Job_Percentage"] = (
    trend_summary["Total_Jobs"] /
    trend_summary["Total_Jobs"].sum() * 100
).round(2)

# -----------------------------
# Save Report
# -----------------------------
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "trend_analysis.csv"

trend_summary.to_csv(output_file, index=False)

# -----------------------------
# Display Results
# -----------------------------
print("=" * 60)
print("HIRING TREND ANALYTICS REPORT")
print("=" * 60)

print(trend_summary)

print(f"\nTotal Months Analyzed: {trend_summary.shape[0]}")

print(f"\nReport saved successfully to:\n{output_file}")