import pandas as pd
from pathlib import Path

# -----------------------------
# Load Dataset
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

data_path = BASE_DIR / "data" / "cleaned" / "job_postings_cleaned.csv"

df = pd.read_csv(data_path)

# -----------------------------
# Company Analysis
# -----------------------------

company_summary = (
    df.groupby("company")
      .agg(
          Total_Jobs=("id", "count"),
          Unique_Roles=("title", "nunique"),
          Locations=("location", "nunique")
      )
      .sort_values("Total_Jobs", ascending=False)
      .reset_index()
)

company_summary["Job_Percentage"] = (
    company_summary["Total_Jobs"] /
    company_summary["Total_Jobs"].sum()
) * 100

company_summary["Job_Percentage"] = (
    company_summary["Job_Percentage"]
    .round(2)
)

# -----------------------------
# Save Report
# -----------------------------

reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "company_analysis.csv"

company_summary.to_csv(output_file, index=False)

print("=" * 50)
print("Company Analytics Generated Successfully")
print("=" * 50)

print(company_summary.head(10))

print(f"\nReport saved to:\n{output_file}")