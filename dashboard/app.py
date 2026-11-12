import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="VELOOP | Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# DATA PATH
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

@st.cache_data
def load_data(filename):
    file_path = DATA_DIR / filename

    if file_path.exists():
        return pd.read_csv(file_path)

    return pd.DataFrame()

users = load_data("users.csv")
daily_activity = load_data("daily_activity.csv")
daily = daily_activity
sessions = load_data("sessions.csv")
tasks = load_data("task_activity.csv")
events = load_data("feature_events.csv")
features = load_data("feature_usage.csv")
milestones = load_data("milestones.csv")

# ---------------------------------
# CUSTOM DARK THEME
# ---------------------------------

# RESPONSIVE LIGHT AND DARK THEME
st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    min-width: 260px;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: var(--secondary-background-color);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

/* Headings and text */
h1, h2, h3, p, label {
    color: var(--text-color);
}

/* Dashboard spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Charts */
[data-testid="stVegaLiteChart"],
[data-testid="stPlotlyChart"],
[data-testid="stArrowVegaLiteChart"] {
    width: 100%;
}

/* Tables */
[data-testid="stDataFrame"] {
    width: 100%;
}

/* Responsive tablet */
@media screen and (max-width: 992px) {
    .block-container {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
}

/* Responsive mobile */
@media screen and (max-width: 768px) {
    .block-container {
        padding: 1rem 0.75rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    [data-testid="stMetric"] {
        padding: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("VELOOP")
st.sidebar.caption("REWARDS ANALYTICS PLATFORM")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "User Engagement",
        "Task Performance",
        "Feature Usage",
        "Data Quality"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Data Source: Simulated Datasets")
st.sidebar.caption("Analytics Dashboard v1.0")

# ---------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------
if page == "Executive Overview":

    st.title("Executive Overview")
    st.caption("Platform performance at a glance")

    total_users = users["user_id"].nunique() if not users.empty else 0

    active_users = (
        daily["user_id"].nunique()
        if not daily.empty else 0
    )

    total_sessions = (
        sessions["session_id"].nunique()
        if not sessions.empty else 0
    )

    total_events = (
        events["event_id"].nunique()
        if not events.empty else 0
    )

    avg_duration = (
        sessions["session_duration_seconds"].mean() / 60
        if not sessions.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Users", f"{total_users:,}")
    col2.metric("Active Users", f"{active_users:,}")
    col3.metric("Total Sessions", f"{total_sessions:,}")
    col4.metric("Total Events", f"{total_events:,}")

    st.divider()

    col5, col6 = st.columns(2)

    col5.metric(
        "Avg. Raw Session Duration",
        f"{avg_duration:.2f} min"
    )

    col6.metric(
        "Available Features",
        f"{len(features):,}"
    )

    st.info(
        "Rewards, Wallet, Withdrawals and Referral "
        "analytics are pending because their datasets "
        "are not currently available."
    )

# ---------------------------------
# OTHER PAGES - INITIAL PLACEHOLDERS
# ---------------------------------
elif page == "User Engagement":

    st.title("User Engagement")
    st.caption("Analyze daily user activity and session behaviour")

    # Daily Active Users
    dau = daily_activity.groupby("activity_date")["user_id"].nunique()

    # Average Session Duration
    avg_duration = daily_activity["session_duration_minutes"].mean()

    # Total Active Days
    active_days = daily_activity["activity_date"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Daily Active Users (Average)", round(dau.mean()))
    col2.metric("Avg. Daily Session Duration", f"{avg_duration:.2f} min")
    col3.metric("Active Dates", active_days)
    # Engagement KPIs
    total_events = daily_activity["event_count"].sum()
    avg_events = daily_activity["event_count"].mean()

    st.divider()

    kpi1, kpi2 = st.columns(2)

    kpi1.metric("Total User Events", f"{total_events:,}")
    kpi2.metric("Avg. Events per Active Day", f"{avg_events:.2f}")
    st.divider()

    st.subheader("Daily Active Users Trend")

    st.line_chart(dau)

    st.subheader("Daily Session Duration Trend")

    duration_trend = daily_activity.groupby("activity_date")[
        "session_duration_minutes"
    ].mean()

    st.line_chart(duration_trend)
    # Weekly Active Users Trend    
    st.subheader("Weekly Active Users Trend")

    weekly_data = daily_activity.copy()

    weekly_data["activity_date"] = pd.to_datetime(
    weekly_data["activity_date"]
    )

    weekly_active_users = (
    weekly_data
    .groupby(
    weekly_data["activity_date"].dt.to_period("W")
    )["user_id"]
    .nunique()
    )
    weekly_active_users = weekly_active_users.iloc[:-1]
    weekly_active_users.index = weekly_active_users.index.astype(str)

    st.line_chart(weekly_active_users)

elif page == "Task Performance":

    st.title("Task Performance")
    st.caption("Task completion and failure analytics")

    # Task status counts
    status_counts = tasks["task_status"].value_counts()

    total_tasks = len(tasks)
    completed = status_counts.get("Completed", 0)
    failed = status_counts.get("Failed", 0)
    abandoned = status_counts.get("Abandoned", 0)

    completion_rate = (completed / total_tasks * 100) if total_tasks else 0

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", f"{total_tasks:,}")
    col2.metric("Completed Tasks", f"{completed:,}")
    col3.metric("Failed Tasks", f"{failed:,}")
    col4.metric("Completion Rate", f"{completion_rate:.1f}%")

    st.divider()

    # Task Status Chart
    st.subheader("Task Status Distribution")
    st.bar_chart(status_counts)

    # Failure Reasons
    st.subheader("Task Failure Reasons")

    failure_data = tasks[
        tasks["task_status"] == "Failed"
    ]["failure_reason"].value_counts()

    st.bar_chart(failure_data)


elif page == "Feature Usage":
    st.title("Feature Usage")
    st.caption("Analyze feature adoption and user activity")

    # Feature summary
    total_features = features["feature_name"].nunique()
    total_events = int(features["total_events"].sum())
    unique_users = events["user_id"].nunique()

    top_feature = features.sort_values(
        "total_events", ascending=False
    ).iloc[0]["feature_name"]

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Available Features", total_features)
    col2.metric("Total Events", f"{total_events:,}")
    col3.metric("Unique Users", f"{unique_users:,}")

    st.divider()

    # Most Used Features
    st.subheader("Most Used Features")

    feature_chart = features.sort_values(
        "total_events", ascending=False
    ).set_index("feature_name")[["total_events"]]

    st.bar_chart(feature_chart)

    st.divider()

    # Feature Ranking
    st.subheader("Feature Usage Ranking")

    feature_table = features.sort_values(
        "total_events", ascending=False
    )

    st.dataframe(feature_table, use_container_width=True)

    st.success(f"Most used feature: {top_feature}")



elif page == "Data Quality":
    st.title("Data Quality")
    st.caption("Dataset profiling and data quality monitoring")

    # Dataset summary
    datasets = {
        "Users": users,
        "Daily Activity": daily,
        "Sessions": sessions,
        "Task Activity": tasks,
        "Feature Events": events,
        "Feature Usage": features,
        "Milestones": milestones
    }

    # Calculate quality metrics
    quality_data = []

    for name, df in datasets.items():
        quality_data.append({
            "Dataset": name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum())
        })

    quality_df = pd.DataFrame(quality_data)

    total_rows = quality_df["Rows"].sum()
    total_missing = quality_df["Missing Values"].sum()
    total_duplicates = quality_df["Duplicate Rows"].sum()

    st.divider()

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Datasets", len(datasets))
    col2.metric("Total Records", f"{total_rows:,}")
    col3.metric("Missing Values", f"{total_missing:,}")
    col4.metric("Duplicate Rows", f"{total_duplicates:,}")

    st.divider()

    # Dataset Quality Summary
    st.subheader("Dataset Quality Summary")
    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Missing Values Chart
    st.subheader("Missing Values by Dataset")

    missing_chart = quality_df[
        quality_df["Missing Values"] > 0
    ].set_index("Dataset")["Missing Values"]

    if not missing_chart.empty:
        st.bar_chart(missing_chart)
    else:
        st.success("No missing values found.")

    st.divider()

    # Missing Values by Column
    st.subheader("Missing Values by Column")

    missing_details = []

    for name, df in datasets.items():
        missing_counts = df.isnull().sum()

        for column, count in missing_counts.items():
            if count > 0:
                missing_details.append({
                    "Dataset": name,
                    "Column": column,
                    "Missing Values": int(count)
                })

    if missing_details:
        st.dataframe(
            pd.DataFrame(missing_details),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("All columns are complete.")

    st.divider()

    # Additional Data Quality Findings
    st.subheader("Data Quality Findings")

    findings = pd.DataFrame([
        {
            "Finding": "Completed tasks exceed daily task count",
            "Affected Records": 423,
            "Status": "Open - Investigation Required"
        },
        {
            "Finding": "Daily task count differs from raw task activity",
            "Affected Records": 282,
            "Status": "Open - Definition Verification Required"
        },
        {
            "Finding": "Daily session duration exceeds raw session duration by more than expected",
            "Affected Records": 15,
            "Status": "Open - Investigation Required"
        },
        {
            "Finding": "Daily records unmatched using session start date",
            "Affected Records": 5,
            "Status": "Open - Date Attribution Verification"
        },
        {
            "Finding": "Event sequence non-increasing transitions",
            "Affected Records": 15556,
            "Status": "Open - Event Order Verification"
        }
    ])

    st.dataframe(
        findings,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Note: Findings are based on simulated data audits. "
        "Affected record counts represent investigation results, "
        "not confirmed production defects."
    )

    st.info(
        "Data source: Simulated datasets. "
        "Missing values and duplicate rows are calculated "
        "from the processed CSV files."
    )


st.sidebar.divider()
st.sidebar.caption("VELOOP Rewards Analytics | 2026")
