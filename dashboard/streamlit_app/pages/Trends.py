
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import load_jobs


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Hiring Trends | CareerLens AI",
    page_icon="📈",
    layout="wide",
)

BG = "#0B1120"
CARD = "#111C30"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
BLUE = "#60A5FA"
TEAL = "#2DD4BF"
PURPLE = "#A78BFA"
BORDER = "#263449"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}
    [data-testid="stSidebar"] {{
        background: #0F172A;
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}
    .trend-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 20px;
        min-height: 118px;
    }}
    .trend-label {{
        color: {MUTED};
        font-size: 13px;
        margin-bottom: 10px;
    }}
    .trend-value {{
        color: {TEXT};
        font-size: 27px;
        font-weight: 700;
    }}
    .trend-note {{
        color: {MUTED};
        font-size: 12px;
        margin-top: 8px;
    }}
    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

CHART_LAYOUT = dict(
    paper_bgcolor=CARD,
    plot_bgcolor=CARD,
    font=dict(color=TEXT),
    margin=dict(l=25, r=20, t=45, b=25),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
    ),
)


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="trend-card">
            <div class="trend-label">{label}</div>
            <div class="trend-value">{value}</div>
            <div class="trend-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    f"""
    <div style="margin-bottom:22px;">
        <div style="color:{TEAL};font-size:12px;font-weight:700;
                    letter-spacing:2px;">
            CAREERLENS AI / ANALYTICS
        </div>
        <h1 style="color:{TEXT};margin:8px 0 4px 0;">
            Hiring Trends
        </h1>
        <p style="color:{MUTED};font-size:15px;">
            Explore posting activity, monthly hiring patterns,
            and the sources publishing job opportunities.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
try:
    jobs = load_jobs()
except Exception as error:
    st.error(
        "Could not load job data from PostgreSQL. "
        "Check your database connection and utils.py."
    )
    with st.expander("Technical details"):
        st.code(str(error))
    st.stop()

if jobs.empty:
    st.warning("No job postings were found in the database.")
    st.stop()

required_columns = [
    "job_id",
    "title",
    "company_name",
    "location_name",
    "source_name",
    "date_posted",
]

missing_columns = [
    column for column in required_columns
    if column not in jobs.columns
]

if missing_columns:
    st.error(
        "The job data is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

jobs["date_posted"] = pd.to_datetime(
    jobs["date_posted"],
    errors="coerce",
    utc=True,
).dt.tz_convert(None)

jobs["source_name"] = (
    jobs["source_name"]
    .fillna("Unknown")
    .astype(str)
)

jobs["title"] = jobs["title"].fillna("Untitled position")
jobs["company_name"] = jobs["company_name"].fillna("Unknown company")
jobs["location_name"] = jobs["location_name"].fillna("Unknown location")

valid_dates = jobs.dropna(subset=["date_posted"]).copy()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.markdown("### Filters")

filter_col1, filter_col2, filter_col3 = st.columns([1.3, 1.3, 1])

with filter_col1:
    sources = sorted(jobs["source_name"].unique().tolist())
    selected_sources = st.multiselect(
        "Job posting source",
        options=sources,
        default=sources,
    )

with filter_col2:
    if not valid_dates.empty:
        min_date = valid_dates["date_posted"].min().date()
        max_date = valid_dates["date_posted"].max().date()

        selected_dates = st.date_input(
            "Posting date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        selected_dates = None
        st.caption("No valid posting dates available.")

with filter_col3:
    trend_interval = st.selectbox(
        "Trend interval",
        options=["Monthly", "Weekly", "Daily"],
        index=0,
    )

filtered = jobs[jobs["source_name"].isin(selected_sources)].copy()

if selected_dates and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered = filtered[
        filtered["date_posted"].notna()
        & (filtered["date_posted"].dt.date >= start_date)
        & (filtered["date_posted"].dt.date <= end_date)
    ]

filtered_valid_dates = filtered.dropna(subset=["date_posted"]).copy()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
total_postings = len(filtered)
dated_postings = len(filtered_valid_dates)
source_count = filtered["source_name"].nunique()

if not filtered_valid_dates.empty:
    latest_date = filtered_valid_dates["date_posted"].max().strftime(
        "%d %b %Y"
    )
else:
    latest_date = "Unavailable"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card(
        "JOB POSTINGS",
        f"{total_postings:,}",
        "Postings matching your filters",
    )

with kpi2:
    metric_card(
        "POSTINGS WITH DATES",
        f"{dated_postings:,}",
        "Usable posting dates",
    )

with kpi3:
    metric_card(
        "ACTIVE SOURCES",
        f"{source_count:,}",
        "Sources in the selected data",
    )

with kpi4:
    metric_card(
        "LATEST POSTING DATE",
        latest_date,
        "Latest valid date in the filtered data",
    )

st.write("")


# --------------------------------------------------
# HIRING TREND CHART
# --------------------------------------------------
st.markdown("### Posting Activity Over Time")

if filtered_valid_dates.empty:
    st.info(
        "No valid posting dates match your current filters. "
        "Try selecting different sources or checking date_posted "
        "in your dataset."
    )
else:
    if trend_interval == "Monthly":
        filtered_valid_dates["period"] = (
            filtered_valid_dates["date_posted"].dt.to_period("M")
            .dt.to_timestamp()
        )
        date_format = "%b %Y"

    elif trend_interval == "Weekly":
        filtered_valid_dates["period"] = (
            filtered_valid_dates["date_posted"]
            .dt.to_period("W")
            .dt.start_time
        )
        date_format = "%d %b %Y"

    else:
        filtered_valid_dates["period"] = (
            filtered_valid_dates["date_posted"].dt.floor("D")
        )
        date_format = "%d %b %Y"

    trend_data = (
        filtered_valid_dates.groupby("period")
        .size()
        .reset_index(name="postings")
        .sort_values("period")
    )

    fig_trend = px.area(
        trend_data,
        x="period",
        y="postings",
        markers=True,
        title=f"{trend_interval} Job Posting Volume",
        labels={
            "period": "Posting period",
            "postings": "Number of postings",
        },
    )

    fig_trend.update_traces(
        line=dict(color=BLUE, width=3),
        marker=dict(color=TEAL, size=6),
        fillcolor="rgba(96,165,250,0.16)",
    )

    fig_trend.update_layout(**CHART_LAYOUT)
    fig_trend.update_xaxes(
        showgrid=False,
        tickformat=date_format,
        title=None,
    )
    fig_trend.update_yaxes(
        gridcolor=BORDER,
        rangemode="tozero",
        title=None,
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    with st.expander("View posting counts by period"):
        trend_table = trend_data.copy()
        trend_table["period"] = trend_table["period"].dt.strftime(
            date_format
        )
        st.dataframe(
            trend_table.rename(
                columns={
                    "period": "Period",
                    "postings": "Job Postings",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# SOURCE ANALYSIS
# --------------------------------------------------
st.markdown("### Hiring Source Analysis")

source_col1, source_col2 = st.columns([1.15, 1])

source_counts = (
    filtered["source_name"]
    .value_counts()
    .rename_axis("source")
    .reset_index(name="postings")
)

with source_col1:
    st.markdown("#### Postings by Source")

    if source_counts.empty:
        st.info("No source data matches your filters.")
    else:
        fig_source = px.bar(
            source_counts.sort_values("postings"),
            x="postings",
            y="source",
            orientation="h",
            text="postings",
            color="postings",
            color_continuous_scale=["#1E3A5F", BLUE, TEAL],
            labels={
                "source": "Source",
                "postings": "Job postings",
            },
        )

        fig_source.update_traces(
            textposition="outside",
            cliponaxis=False,
        )
        fig_source.update_layout(
            **CHART_LAYOUT,
            coloraxis_showscale=False,
            showlegend=False,
        )
        fig_source.update_xaxes(
            showgrid=True,
            gridcolor=BORDER,
            title=None,
        )
        fig_source.update_yaxes(
            showgrid=False,
            title=None,
        )

        st.plotly_chart(
            fig_source,
            use_container_width=True,
        )

with source_col2:
    st.markdown("#### Source Share")

    if source_counts.empty:
        st.info("No source data matches your filters.")
    else:
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=source_counts["source"],
                    values=source_counts["postings"],
                    hole=0.65,
                    textinfo="percent",
                    marker=dict(
                        colors=[BLUE, TEAL, PURPLE, "#F59E0B", "#F472B6"]
                    ),
                    hovertemplate=(
                        "%{label}<br>"
                        "Postings: %{value:,}<br>"
                        "Share: %{percent}<extra></extra>"
                    ),
                )
            ]
        )

        
        fig_donut.update_layout(
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font=dict(color=TEXT),
            margin=dict(l=25, r=20, t=45, b=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(color=TEXT),
            ),
        )


        st.plotly_chart(
            fig_donut,
            use_container_width=True,
        )

st.write("")


# --------------------------------------------------
# RECENT POSTINGS
# --------------------------------------------------
st.markdown("### Recent Job Postings")

if filtered.empty:
    st.info("No job postings match the selected filters.")
else:
    recent = filtered.sort_values(
        "date_posted",
        ascending=False,
        na_position="last",
    ).head(20).copy()

    recent["date_posted"] = recent["date_posted"].apply(
        lambda value: (
            value.strftime("%d %b %Y")
            if pd.notna(value)
            else "Unknown"
        )
    )

    display_columns = [
        "date_posted",
        "title",
        "company_name",
        "location_name",
        "source_name",
    ]

    recent_display = recent[display_columns].rename(
        columns={
            "date_posted": "Posting Date",
            "title": "Job Title",
            "company_name": "Company",
            "location_name": "Location",
            "source_name": "Source",
        }
    )

    st.dataframe(
        recent_display,
        use_container_width=True,
        hide_index=True,
        height=440,
    )

st.markdown(
    f"""
    <div style="border-top:1px solid {BORDER};
                padding-top:16px;margin-top:24px;
                color:{MUTED};font-size:12px;">
        CareerLens AI · Hiring Intelligence ·
        Trends are based on the available job-posting dataset.
        Posting counts do not necessarily represent unique vacancies
        or confirmed hires.
    </div>
    """,
    unsafe_allow_html=True,
)
