
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import load_jobs


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="CareerLens AI | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================
BG = "#0B1120"
PANEL = "#111C30"
PANEL_LIGHT = "#16243A"
BORDER = "#263750"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
BLUE = "#60A5FA"
TEAL = "#2DD4BF"
PURPLE = "#A78BFA"
AMBER = "#FBBF24"
PINK = "#F472B6"

CHART_COLORS = [BLUE, TEAL, PURPLE, AMBER, PINK]

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: rgba(11, 17, 32, 0.96);
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1550px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    [data-testid="stSidebar"] {{
        background: #0D1728;
        border-right: 1px solid {BORDER};
    }}

    h1, h2, h3 {{
        color: {TEXT} !important;
        letter-spacing: -0.4px;
    }}

    p, label {{
        color: #CBD5E1;
    }}

    .hero {{
        background: linear-gradient(
            120deg,
            #172554 0%,
            #14213D 55%,
            #111C30 100%
        );
        border: 1px solid #2A4166;
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 22px;
    }}

    .eyebrow {{
        color: {BLUE};
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .hero-title {{
        color: #FFFFFF;
        font-size: clamp(25px, 3vw, 34px);
        font-weight: 750;
        line-height: 1.2;
        margin-bottom: 10px;
    }}

    .hero-subtitle {{
        color: #B8C5D9;
        font-size: 14px;
        line-height: 1.7;
        max-width: 760px;
    }}

    .section-title {{
        color: {TEXT};
        font-size: 19px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 4px;
    }}

    .section-subtitle {{
        color: {MUTED};
        font-size: 12px;
        margin-bottom: 14px;
        line-height: 1.6;
    }}

    .kpi-card {{
        position: relative;
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 20px;
        min-height: 132px;
        overflow: hidden;
    }}

    .kpi-card::before {{
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 4px;
        height: 100%;
        background: var(--accent);
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 13px;
    }}

    .kpi-value {{
        color: {TEXT};
        font-size: 30px;
        font-weight: 750;
        line-height: 1.2;
    }}

    .kpi-note {{
        color: #7F93AF;
        font-size: 11px;
        margin-top: 9px;
    }}

    .panel {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 16px 16px 8px 16px;
    }}

    div[data-testid="stPlotlyChart"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 8px;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        border-radius: 9px;
    }}

    .stButton button {{
        border-radius: 9px;
        font-weight: 600;
    }}

    .footer {{
        border-top: 1px solid {BORDER};
        text-align: center;
        color: #7186A5;
        font-size: 11px;
        padding-top: 20px;
        margin-top: 28px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================
@st.cache_data(ttl=60)
def get_dashboard_data():
    return load_jobs()


def section_heading(title, description):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, note, accent):
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(
            family="Arial, sans-serif",
            color=TEXT,
            size=11,
        ),
        margin=dict(l=18, r=28, t=35, b=20),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_color="#FFFFFF",
            bordercolor=BORDER,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=BORDER,
        zeroline=False,
        tickfont=dict(color=MUTED, size=10),
        title_text="",
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color=TEXT, size=10),
        title_text="",
    )

    return fig


def top_counts(data, column, output_name, limit=10):
    result = (
        data[column]
        .fillna("Unknown")
        .astype(str)
        .replace("", "Unknown")
        .value_counts()
        .head(limit)
        .sort_values(ascending=True)
        .rename_axis(output_name)
        .reset_index(name="Job Postings")
    )
    return result


# =========================================================
# LOAD DATA
# =========================================================
try:
    df = get_dashboard_data()

except Exception as error:
    st.error(
        "Unable to load dashboard data from PostgreSQL. "
        "Check your database connection and utils.py."
    )
    with st.expander("Technical details"):
        st.code(str(error))
    st.stop()


if df.empty:
    st.warning("No job posting data is available.")
    st.stop()


required_columns = [
    "title",
    "company_name",
    "location_name",
    "source_name",
    "date_posted",
    "link",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The database query is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# Prepare consistent display values
for column in ["title", "company_name", "location_name", "source_name"]:
    df[column] = df[column].fillna("Unknown").astype(str)

df["date_posted"] = pd.to_datetime(
    df["date_posted"],
    errors="coerce",
    utc=True,
).dt.tz_convert(None)

df["link"] = df["link"].fillna("")


# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">CAREER INTELLIGENCE PLATFORM</div>
        <div class="hero-title">Hiring Analytics Dashboard</div>
        <div class="hero-subtitle">
            Your central view of job-market activity, hiring organizations,
            geographic demand and recruitment sources.
            Explore the data, apply filters and identify hiring patterns.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GLOBAL FILTERS
# =========================================================
section_heading(
    "Explore the data",
    "Use the filters below to update the metrics and charts.",
)

filter1, filter2, filter3 = st.columns([1.1, 1.1, 1.4])

with filter1:
    source_options = sorted(df["source_name"].unique().tolist())
    selected_sources = st.multiselect(
        "Recruitment sources",
        options=source_options,
        default=source_options,
        help="Choose the sources to include in the dashboard.",
    )

with filter2:
    location_options = sorted(df["location_name"].unique().tolist())
    selected_locations = st.multiselect(
        "Locations",
        options=location_options,
        help="Leave empty to include every location.",
    )

with filter3:
    dated_rows = df.dropna(subset=["date_posted"])

    if not dated_rows.empty:
        minimum_date = dated_rows["date_posted"].min().date()
        maximum_date = dated_rows["date_posted"].max().date()

        selected_date_range = st.date_input(
            "Posting date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
        )
    else:
        selected_date_range = None
        st.caption("No valid posting dates are available.")


filtered_df = df[df["source_name"].isin(selected_sources)].copy()

if selected_locations:
    filtered_df = filtered_df[
        filtered_df["location_name"].isin(selected_locations)
    ]

if (
    selected_date_range
    and len(selected_date_range) == 2
):
    start_date, end_date = selected_date_range

    filtered_df = filtered_df[
        filtered_df["date_posted"].notna()
        & (
            filtered_df["date_posted"].dt.date
            >= start_date
        )
        & (
            filtered_df["date_posted"].dt.date
            <= end_date
        )
    ]


st.write("")


# =========================================================
# KPI CARDS
# =========================================================
total_jobs = len(filtered_df)
total_companies = filtered_df["company_name"].nunique()
total_locations = filtered_df["location_name"].nunique()
total_sources = filtered_df["source_name"].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")

with kpi1:
    metric_card(
        "TOTAL JOB POSTINGS",
        f"{total_jobs:,}",
        "Matching the selected filters",
        BLUE,
    )

with kpi2:
    metric_card(
        "COMPANIES",
        f"{total_companies:,}",
        "Unique organizations in results",
        TEAL,
    )

with kpi3:
    metric_card(
        "LOCATIONS",
        f"{total_locations:,}",
        "Distinct locations in results",
        PURPLE,
    )

with kpi4:
    metric_card(
        "JOB SOURCES",
        f"{total_sources:,}",
        "Sources in the selected results",
        AMBER,
    )


if filtered_df.empty:
    st.info(
        "No job postings match your filters. "
        "Try selecting more sources or locations, "
        "or expanding the date range."
    )
    st.stop()


# =========================================================
# TOP COMPANIES AND LOCATIONS
# =========================================================
st.write("")
section_heading(
    "Hiring Market Overview",
    "Compare the organizations and locations with the highest "
    "number of job postings in the selected data.",
)

left, right = st.columns(2, gap="large")

with left:
    company_counts = top_counts(
        filtered_df,
        "company_name",
        "Company",
        limit=10,
    )

    fig_companies = px.bar(
        company_counts,
        x="Job Postings",
        y="Company",
        orientation="h",
        text="Job Postings",
        color_discrete_sequence=[BLUE],
        hover_data={"Job Postings": True, "Company": True},
    )

    fig_companies.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Job postings: %{x:,}"
            "<extra></extra>"
        ),
    )

    style_chart(fig_companies, height=390)
    fig_companies.update_layout(
        margin=dict(l=15, r=38, t=22, b=25),
    )

    section_heading(
        "Top Hiring Companies",
        "Organizations with the most job listings.",
    )

    st.plotly_chart(
        fig_companies,
        use_container_width=True,
        config={"displayModeBar": False},
    )


with right:
    location_counts = top_counts(
        filtered_df,
        "location_name",
        "Location",
        limit=10,
    )

    fig_locations = px.bar(
        location_counts,
        x="Job Postings",
        y="Location",
        orientation="h",
        text="Job Postings",
        color_discrete_sequence=[TEAL],
    )

    fig_locations.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Job postings: %{x:,}"
            "<extra></extra>"
        ),
    )

    style_chart(fig_locations, height=390)
    fig_locations.update_layout(
        margin=dict(l=15, r=38, t=22, b=25),
    )

    section_heading(
        "Top Hiring Locations",
        "Locations with the highest posting volume.",
    )

    st.plotly_chart(
        fig_locations,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# RECRUITMENT SOURCE ANALYSIS
# =========================================================
st.write("")
section_heading(
    "Recruitment Source Analysis",
    "Understand how job listings are distributed across the sources.",
)

source_counts = (
    filtered_df["source_name"]
    .value_counts()
    .rename_axis("Source")
    .reset_index(name="Job Postings")
)

source_left, source_right = st.columns([1, 1.35], gap="large")

with source_left:
    fig_sources = go.Figure(
        data=[
            go.Pie(
                labels=source_counts["Source"],
                values=source_counts["Job Postings"],
                hole=0.68,
                sort=False,
                marker=dict(
                    colors=CHART_COLORS,
                    line=dict(color=PANEL, width=3),
                ),
                textinfo="percent",
                textfont=dict(color="#FFFFFF", size=12),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Job postings: %{value:,}<br>"
                    "Share: %{percent}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig_sources.update_layout(
        height=330,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT, size=11),
        margin=dict(l=10, r=10, t=20, b=55),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.16,
            xanchor="center",
            x=0.5,
            font=dict(color=MUTED, size=10),
        ),
    )

    section_heading(
        "Source Share",
        "Percentage of filtered job postings by source.",
    )

    st.plotly_chart(
        fig_sources,
        use_container_width=True,
        config={"displayModeBar": False},
    )


with source_right:
    source_bar_data = source_counts.sort_values(
        "Job Postings",
        ascending=True,
    )

    fig_source_bars = px.bar(
        source_bar_data,
        x="Job Postings",
        y="Source",
        orientation="h",
        text="Job Postings",
        color_discrete_sequence=[PURPLE],
    )

    fig_source_bars.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Job postings: %{x:,}"
            "<extra></extra>"
        ),
    )

    style_chart(fig_source_bars, height=330)
    fig_source_bars.update_layout(
        margin=dict(l=15, r=38, t=22, b=25),
    )

    section_heading(
        "Postings by Source",
        "Compare the number of listings contributed by each source.",
    )

    st.plotly_chart(
        fig_source_bars,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# RECENT JOB POSTINGS
# =========================================================
st.write("")
section_heading(
    "Job Posting Explorer",
    "Search the filtered results and inspect individual job listings.",
)

search_col, source_col, rows_col = st.columns([2, 1, 1])

with search_col:
    search_text = st.text_input(
        "Search jobs",
        placeholder="Search title, company or location...",
    )

with source_col:
    table_sources = ["All sources"] + sorted(
        filtered_df["source_name"].unique().tolist()
    )

    table_source = st.selectbox(
        "Table source filter",
        table_sources,
    )

with rows_col:
    display_limit = st.selectbox(
        "Rows to display",
        [10, 25, 50, 100],
        index=1,
    )


table_df = filtered_df.copy()

if search_text.strip():
    search_mask = (
        table_df["title"].str.contains(
            search_text, case=False, na=False, regex=False
        )
        | table_df["company_name"].str.contains(
            search_text, case=False, na=False, regex=False
        )
        | table_df["location_name"].str.contains(
            search_text, case=False, na=False, regex=False
        )
    )

    table_df = table_df[search_mask]

if table_source != "All sources":
    table_df = table_df[
        table_df["source_name"] == table_source
    ]

table_df = table_df.sort_values(
    "date_posted",
    ascending=False,
    na_position="last",
)

st.caption(
    f"Showing {min(len(table_df), display_limit):,} of "
    f"{len(table_df):,} matching job postings."
)

display_df = table_df[
    [
        "title",
        "company_name",
        "location_name",
        "source_name",
        "date_posted",
        "link",
    ]
].head(display_limit).copy()

display_df = display_df.rename(
    columns={
        "title": "Job Title",
        "company_name": "Company",
        "location_name": "Location",
        "source_name": "Source",
        "date_posted": "Date Posted",
        "link": "Job Link",
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=440,
    column_config={
        "Job Title": st.column_config.TextColumn(
            "Job Title",
            width="large",
        ),
        "Company": st.column_config.TextColumn("Company"),
        "Location": st.column_config.TextColumn("Location"),
        "Source": st.column_config.TextColumn("Source"),
        "Date Posted": st.column_config.DateColumn(
            "Date Posted",
            format="DD MMM YYYY",
        ),
        "Job Link": st.column_config.LinkColumn(
            "Open Job",
            display_text="View listing ↗",
        ),
    },
)


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        CAREERLENS AI · HIRING INTELLIGENCE · POWERED BY POSTGRESQL
    </div>
    """,
    unsafe_allow_html=True,
)
