
import re

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import load_jobs


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CareerLens AI | Skills Analytics",
    page_icon="🧠",
    layout="wide",
)


# =====================================================
# PROFESSIONAL STYLING
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0B1120;
        color: #E5E7EB;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #F8FAFC !important;
    }

    p, label {
        color: #CBD5E1;
    }

    .page-hero {
        background: linear-gradient(120deg, #172554, #14213D, #162033);
        border: 1px solid #263754;
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 25px;
    }

    .eyebrow {
        color: #93C5FD;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 750;
    }

    .hero-description {
        color: #B8C5D9;
        font-size: 14px;
        margin-top: 8px;
    }

    .metric-card {
        background: #111C30;
        border: 1px solid #263750;
        border-radius: 14px;
        padding: 20px;
        min-height: 110px;
    }

    .metric-label {
        color: #9CAEC6;
        font-size: 12px;
        font-weight: 600;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 30px;
        font-weight: 750;
        margin-top: 10px;
    }

    .section-heading {
        color: #F1F5F9;
        font-size: 20px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 6px;
    }

    .section-caption {
        color: #91A2BA;
        font-size: 12px;
        margin-bottom: 14px;
    }

    div[data-testid="stPlotlyChart"] {
        background: #111C30;
        border: 1px solid #25354D;
        border-radius: 14px;
        padding: 8px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263750;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #25354D !important;
        margin: 25px 0;
    }

    section[data-testid="stSidebar"] {
        background: #0D1728;
        border-right: 1px solid #24334A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="page-hero">
        <div class="eyebrow">CAREER INTELLIGENCE PLATFORM</div>
        <div class="hero-title">In-Demand Skills Analytics</div>
        <div class="hero-description">
            Discover the technical and analytical skills mentioned
            most frequently across your job-posting dataset.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# LOAD JOB DATA
# =====================================================

try:
    df = load_jobs()

    if df.empty:
        st.warning("No job posting data is available.")
        st.stop()

except Exception as error:
    st.error("Unable to load skills data from PostgreSQL.")
    st.exception(error)
    st.stop()


# =====================================================
# SKILL KEYWORD CATALOG
# =====================================================

SKILLS = {
    "Python": [r"\bpython\b"],
    "SQL": [r"\bsql\b"],
    "Excel": [r"\bexcel\b", r"\bmicrosoft excel\b"],
    "Power BI": [r"\bpower\s*bi\b", r"\bpowerbi\b"],
    "Tableau": [r"\btableau\b"],
    "Machine Learning": [r"\bmachine learning\b"],
    "Statistics": [r"\bstatistics\b", r"\bstatistical analysis\b"],
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "PostgreSQL": [r"\bpostgres(?:ql)?\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "Azure": [r"\bazure\b", r"\bmicrosoft azure\b"],
    "R Programming": [r"\br programming\b", r"\br language\b"],
    "Apache Spark": [r"\bapache spark\b", r"\bspark\b"],
    "Data Visualization": [r"\bdata visualization\b", r"\bdata visualisation\b"],
    "ETL": [r"\betl\b", r"\bextract transform load\b"],
    "DAX": [r"\bdax\b", r"\bdata analysis expressions\b"],
    "Power Query": [r"\bpower query\b"],
    "Data Modeling": [r"\bdata modeling\b", r"\bdata modelling\b"],
    "Communication": [r"\bcommunication skills\b", r"\bcommunicate effectively\b"],
}


# =====================================================
# ANALYZE SKILL MENTIONS
# =====================================================

@st.cache_data(ttl=60)
def calculate_skill_counts(data):
    text_series = (
        data["title"].fillna("").astype(str)
        + " "
        + data["description"].fillna("").astype(str)
    ).str.lower()

    results = []

    for skill, patterns in SKILLS.items():
        pattern = re.compile("|".join(patterns), re.IGNORECASE)

        count = int(
            text_series.apply(
                lambda text: bool(pattern.search(text))
            ).sum()
        )

        results.append({
            "Skill": skill,
            "Jobs Mentioning Skill": count,
            "Percentage of Jobs": round(
                count / max(len(data), 1) * 100, 1
            ),
        })

    return pd.DataFrame(results).sort_values(
        "Jobs Mentioning Skill",
        ascending=False,
    )


skills_df = calculate_skill_counts(df)


# =====================================================
# KPI CARDS
# =====================================================

total_jobs = len(df)
skills_tracked = len(SKILLS)

if not skills_df.empty:
    top_skill = skills_df.iloc[0]["Skill"]
    top_skill_count = int(skills_df.iloc[0]["Jobs Mentioning Skill"])
else:
    top_skill = "N/A"
    top_skill_count = 0

m1, m2, m3 = st.columns(3)

metrics = [
    (m1, "JOBS ANALYZED", f"{total_jobs:,}"),
    (m2, "SKILLS TRACKED", f"{skills_tracked:,}"),
    (m3, "MOST MENTIONED SKILL", top_skill),
]

for column, label, value in metrics:
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =====================================================
# TOP SKILLS CHART
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Most Requested Skills</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">Ranked by the number of job postings mentioning each skill.</div>',
    unsafe_allow_html=True,
)

top_n = st.selectbox(
    "Number of skills to display",
    [5, 10, 15, 20],
    index=1,
)

top_skills = (
    skills_df.head(top_n)
    .sort_values("Jobs Mentioning Skill", ascending=True)
)

fig = px.bar(
    top_skills,
    x="Jobs Mentioning Skill",
    y="Skill",
    orientation="h",
    text="Jobs Mentioning Skill",
    color_discrete_sequence=["#60A5FA"],
    hover_data=["Percentage of Jobs"],
)

fig.update_traces(
    textposition="outside",
    cliponaxis=False,
    marker_line_width=0,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Jobs mentioning skill: %{x}<extra></extra>"
    ),
)

fig.update_layout(
    height=max(350, top_n * 35),
    paper_bgcolor="#111C30",
    plot_bgcolor="#111C30",
    font=dict(color="#CBD5E1", size=11),
    margin=dict(l=15, r=35, t=20, b=25),
    showlegend=False,
)

fig.update_xaxes(
    showgrid=True,
    gridcolor="#27364D",
    zeroline=False,
    title_text="Number of Job Postings",
)

fig.update_yaxes(
    showgrid=False,
    title_text="",
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False},
)


# =====================================================
# SKILL SEARCH AND DIRECTORY
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Skill Directory</div>',
    unsafe_allow_html=True,
)

search = st.text_input(
    "Search skills",
    placeholder="For example: Python, SQL, Power BI...",
)

filtered = skills_df.copy()

if search.strip():
    filtered = filtered[
        filtered["Skill"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Skill": st.column_config.TextColumn("Skill"),
        "Jobs Mentioning Skill": st.column_config.NumberColumn(
            "Jobs Mentioning Skill",
            format="%d",
        ),
        "Percentage of Jobs": st.column_config.NumberColumn(
            "Percentage of Jobs",
            format="%.1f%%",
        ),
    },
)

st.caption(
    "Methodology: each job is counted at most once per skill. "
    "Counts are based on keyword matches in job titles and descriptions; "
    "they are not a semantic assessment of skill requirements."
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7186A5;
        font-size:11px;
        padding:25px 0 5px 0;
    ">
        CAREERLENS AI · SKILLS INTELLIGENCE · POWERED BY POSTGRESQL
    </div>
    """,
    unsafe_allow_html=True,
)
