
import pandas as pd
import streamlit as st
from sqlalchemy import text
from config.database import engine


@st.cache_data(ttl=60)
def load_query(query):
    """Load data from PostgreSQL using the existing project connection."""
    with engine.connect() as connection:
        return pd.read_sql_query(text(query), connection)


def load_jobs():
    return load_query("""
        SELECT
            j.job_id,
            j.title,
            c.company_name,
            l.location_name,
            s.source_name,
            j.date_posted,
            j.description,
            j.link
        FROM job_postings j
        LEFT JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN locations l ON j.location_id = l.location_id
        LEFT JOIN sources s ON j.source_id = s.source_id
    """)
