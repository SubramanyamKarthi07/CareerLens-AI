
import streamlit as st
import plotly.express as px

from utils import load_jobs


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CareerLens AI | Locations",
    page_icon="📍",
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
        <div class="hero-title">Job Location Analytics</div>
        <div class="hero-description">
            Explore geographic hiring demand, compare locations,
            and identify where job opportunities are concentrated.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# LOAD DATABASE DATA
# =====================================================

try:
    df = load_jobs()

    if df.empty:
        st.warning("No job posting data is available.")
        st.stop()

except Exception as error:
    st.error("Unable to load location data from PostgreSQL.")
    st.exception(error)
    st.stop()


# =====================================================
# LOCATION STATISTICS
# =====================================================

location_counts = (
    df.dropna(subset=["location_name"])
    .groupby("location_name")
    .size()
    .reset_index(name="Job Postings")
    .sort_values("Job Postings", ascending=False)
)

total_locations = df["location_name"].nunique()
total_jobs = len(df)

top_location = (
    location_counts.iloc[0]["location_name"]
    if not location_counts.empty
    else "N/A"
)

top_location_jobs = (
    int(location_counts.iloc[0]["Job Postings"])
    if not location_counts.empty
    else 0
)

m1, m2, m3 = st.columns(3)

metrics = [
    (m1, "UNIQUE LOCATIONS", f"{total_locations:,}"),
    (m2, "TOTAL JOB POSTINGS", f"{total_jobs:,}"),
    (m3, "TOP LOCATION JOBS", f"{top_location_jobs:,}"),
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
# LOCATION SEARCH
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Explore Locations</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">Search location names and filter job-posting volumes.</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns([2, 1])

with c1:
    search = st.text_input(
        "Search location",
        placeholder="Enter a city, region, or country...",
    )

with c2:
    minimum_jobs = st.number_input(
        "Minimum job postings",
        min_value=1,
        max_value=max(1, total_jobs),
        value=1,
        step=1,
    )

filtered = location_counts.copy()

if search.strip():
    filtered = filtered[
        filtered["location_name"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

filtered = filtered[
    filtered["Job Postings"] >= minimum_jobs
]

st.caption(f"{len(filtered):,} locations match your filters.")


# =====================================================
# TOP LOCATIONS CHART
# =====================================================

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown(
        '<div class="section-heading">Top 10 Hiring Locations</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-caption">Locations ranked by job-posting count.</div>',
        unsafe_allow_html=True,
    )

    top10 = (
        location_counts.head(10)
        .sort_values("Job Postings", ascending=True)
    )

    fig = px.bar(
        top10,
        x="Job Postings",
        y="location_name",
        orientation="h",
        text="Job Postings",
        color_discrete_sequence=["#2DD4BF"],
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
        '<div class="section-heading">Location Snapshot</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-caption">A quick view of geographic job demand.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">LEADING LOCATION</div>
            <div style="color:#F8FAFC;font-size:24px;font-weight:700;margin-top:12px;">
                {top_location}
            </div>
            <div style="color:#91A2BA;font-size:12px;margin-top:8px;">
                {top_location_jobs:,} job postings
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if not location_counts.empty:
        average = location_counts["Job Postings"].mean()
        median = location_counts["Job Postings"].median()

        st.metric("Average postings per location", f"{average:.1f}")
        st.metric("Median postings per location", f"{median:.0f}")

        top10_share = (
            location_counts.head(10)["Job Postings"].sum()
            / max(1, total_jobs)
            * 100
        )

        st.metric("Share from top 10 locations", f"{top10_share:.1f}%")


# =====================================================
# LOCATION DIRECTORY
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">Location Directory</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">All locations and their associated job-posting counts.</div>',
    unsafe_allow_html=True,
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "location_name": st.column_config.TextColumn("Location"),
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
        CAREERLENS AI · LOCATION INTELLIGENCE · POWERED BY POSTGRESQL
    </div>
    """,
    unsafe_allow_html=True,
)
