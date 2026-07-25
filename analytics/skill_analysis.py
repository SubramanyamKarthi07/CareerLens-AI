import pandas as pd
from pathlib import Path
from collections import Counter
import re

# -----------------------------
# Load Dataset
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

data_path = BASE_DIR / "data" / "cleaned" / "job_postings_cleaned.csv"

df = pd.read_csv(data_path)

# -----------------------------
# Handle Missing Descriptions
# -----------------------------
df["description"] = df["description"].fillna("").str.lower()

# -----------------------------
# Skills Dictionary
# -----------------------------
skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "aws",
    "azure",
    "gcp",
    "spark",
    "hadoop",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "statistics",
    "data visualization",
    "etl",
    "postgresql"
]

# -----------------------------
# Count Skills
# -----------------------------
skill_counter = Counter()

for description in df["description"]:

    for skill in skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, description):
            skill_counter[skill] += 1

# -----------------------------
# Convert to DataFrame
# -----------------------------
skill_df = pd.DataFrame(
    skill_counter.items(),
    columns=["Skill", "Frequency"]
)

skill_df = skill_df.sort_values(
    by="Frequency",
    ascending=False
)

# -----------------------------
# Percentage
# -----------------------------
skill_df["Percentage"] = (
    skill_df["Frequency"] /
    len(df) * 100
).round(2)

# -----------------------------
# Save Report
# -----------------------------
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "skill_analysis.csv"

skill_df.to_csv(output_file, index=False)

# -----------------------------
# Display Results
# -----------------------------
print("=" * 60)
print("SKILL INTELLIGENCE REPORT")
print("=" * 60)

print(skill_df.head(20))

print("\nTotal Skills Found:", len(skill_df))

print(f"\nReport saved to:\n{output_file}")