import pandas as pd
from sqlalchemy import text
from config.database import engine


def load_dimension(table_name, column_name, values):
    """Load unique values into a dimension table."""

    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table_name}"))

        for value in sorted(values):
            conn.execute(
                text(f"""
                    INSERT INTO {table_name} ({column_name})
                    VALUES (:value)
                """),
                {"value": value},
            )

    print(f"✔ {table_name} loaded ({len(values)} records)")


df = pd.read_csv("data/cleaned/job_postings_cleaned.csv")

print(f"Dataset Loaded ({len(df)} rows)")

load_dimension(
    "companies",
    "company_name",
    df["company"].unique()
)

load_dimension(
    "locations",
    "location_name",
    df["location"].unique()
)

load_dimension(
    "sources",
    "source_name",
    df["source"].unique()
)

# -----------------------------
# Build Lookup Dictionaries
# -----------------------------
with engine.connect() as conn:

    company_lookup = {
        row.company_name: row.company_id
        for row in conn.execute(
            text("SELECT company_id, company_name FROM companies")
        )
    }

    location_lookup = {
        row.location_name: row.location_id
        for row in conn.execute(
            text("SELECT location_id, location_name FROM locations")
        )
    }

    source_lookup = {
        row.source_name: row.source_id
        for row in conn.execute(
            text("SELECT source_id, source_name FROM sources")
        )
    }

print("Lookup dictionaries created.")


# -----------------------------
# Load Job Postings
# -----------------------------
with engine.begin() as conn:

    conn.execute(text("DELETE FROM job_postings"))

    for _, row in df.iterrows():

        conn.execute(
            text("""
                INSERT INTO job_postings
                (
                    title,
                    company_id,
                    location_id,
                    source_id,
                    date_posted,
                    description,
                    link
                )
                VALUES
                (
                    :title,
                    :company_id,
                    :location_id,
                    :source_id,
                    :date_posted,
                    :description,
                    :link
                )
            """),
            {
                "title": row["title"],
                "company_id": company_lookup[row["company"]],
                "location_id": location_lookup[row["location"]],
                "source_id": source_lookup[row["source"]],
                "date_posted": row["date_posted"],
                "description": row["description"],
                "link": row["link"],
            }
        )

print(f"Job Postings Loaded Successfully! ({len(df)} records)")