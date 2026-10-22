
import streamlit as st
import plotly.express as px

from utils import load_jobs


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CareerLens AI | Companies",
    page_icon="🏢",
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
        min-height: 115px;
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
# LOAD DATA
# =====================================================

st.markdown(
    """
    <div class="page-hero">
        <div class="eyebrow">CAREER INTELLIGENCE PLATFORM</div>
        <div class="hero-title">Company Hiring Analytics</div>
        <div class="hero-description">
            Explore hiring activity, compare organizations,
            and discover which companies publish the most jobs.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    df = load_jobs()

    if df.empty:
        st.warning("No job posting data is available.")
        st.stop()

except Exception as error:
    st.error("Unable to load company data from PostgreSQL.")
    st.exception(error)
    st.stop()


# =====================================================
# METRICS
# =====================================================

company_counts = (
    df.dropna(subset=["company_name"])
    .groupby("company_name")
    .size()
    .reset_index(name="Job Postings")
    .sort_values("Job Postings", ascending=False)
)

total_companies = df["company_name"].nunique()
companies_with_jobs = len(company_counts)
total_postings = int(company_counts["Job Postings"].sum())

top_company = (
    company_counts.iloc[0]["company_name"]
    if not company_counts.empty
    else "N/A"
)

m1, m2, m3 = st.columns(3)

metrics = [
    (m1, "TOTAL COMPANIES", f"{total_companies:,}"),
    (m2, "COMPANIES WITH JOBS", f"{companies_with_jobs:,}"),
    (m3, "POSTINGS WITH A COMPANY", f"{total_postings:,}"),
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
# SEARCH AND FILTER
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Explore Companies</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">Search the company directory or filter by hiring volume.</div>',
    unsafe_allow_html=True,
)

filter1, filter2 = st.columns([2, 1])

with filter1:
    search = st.text_input(
        "Search company",
        placeholder="Enter a company name...",
    )

with filter2:
    minimum_jobs = st.number_input(
        "Minimum job postings",
        min_value=1,
        max_value=max(1, total_postings),
        value=1,
        step=1,
    )

filtered = company_counts.copy()

if search.strip():
    filtered = filtered[
        filtered["company_name"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

filtered = filtered[
    filtered["Job Postings"] >= minimum_jobs
]

st.caption(f"{len(filtered):,} companies match your filters.")


# =====================================================
# TOP HIRING COMPANIES
# =====================================================

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown(
        '<div class="section-heading">Top 10 Hiring Companies</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-caption">Ranked by number of available job postings.</div>',
        unsafe_allow_html=True,
    )

    top10 = (
        company_counts.head(10)
        .sort_values("Job Postings", ascending=True)
    )

    fig = px.bar(
        top10,
        x="Job Postings",
        y="company_name",
        orientation="h",
        text="Job Postings",
        color_discrete_sequence=["#60A5FA"],
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Job postings: %{x}<extra></extra>"
        ),
    )

    fig.update_layout(
        height=430,
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
        title_text="Job Postings",
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


with right:
    st.markdown(
        '<div class="section-heading">Hiring Snapshot</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-caption">Quick insights from your dataset.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOP HIRING COMPANY</div>
            <div style="color:#F8FAFC;font-size:23px;font-weight:700;margin-top:12px;">
                {top_company}
            </div>
            <div style="color:#91A2BA;font-size:12px;margin-top:8px;">
                {int(company_counts.iloc[0]["Job Postings"]) if not company_counts.empty else 0}
                job postings
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if not company_counts.empty:
        average_jobs = company_counts["Job Postings"].mean()
        median_jobs = company_counts["Job Postings"].median()

        st.metric("Average postings per company", f"{average_jobs:.1f}")
        st.metric("Median postings per company", f"{median_jobs:.0f}")

        top10_share = (
            company_counts.head(10)["Job Postings"].sum()
            / max(1, total_postings)
            * 100
        )

        st.metric("Share from top 10 companies", f"{top10_share:.1f}%")


# =====================================================
# COMPANY DIRECTORY
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Company Directory</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">Search and sort company-level hiring statistics.</div>',
    unsafe_allow_html=True,
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "company_name": st.column_config.TextColumn("Company"),
        "Job Postings": st.column_config.NumberColumn(
            "Job Postings",
            format="%d",
        ),
    },
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7186A5;
        font-size:11px;
        padding:25px 0 5px 0;
    ">
        CAREERLENS AI · COMPANY INTELLIGENCE · POWERED BY POSTGRESQL
    </div>
    """,
    unsafe_allow_html=True,
)
