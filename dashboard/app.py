import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="VELOOP | Analytics", page_icon="📊", layout="wide")

# ============================================================
# DATA LOADING (original path preserved; extra fallbacks added)
# ============================================================
APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
DATA_DIRS = [
    BASE_DIR / "data" / "processed",   # original location
    APP_DIR / "data" / "processed",
    APP_DIR / "data",
    APP_DIR,
]


@st.cache_data
def load_data(filename):
    for d in DATA_DIRS:
        p = d / filename
        if p.exists():
            return pd.read_csv(p)
    return pd.DataFrame()


users = load_data("users.csv")
daily_activity = load_data("daily_activity.csv")
daily = daily_activity
sessions = load_data("sessions.csv")
tasks = load_data("task_activity.csv")
events = load_data("feature_events.csv")
features = load_data("feature_usage.csv")
milestones = load_data("milestones.csv")

# ============================================================
# THEME
# ============================================================
THEMES = {
    "Light": dict(bg="#f6f7fb", card="#ffffff", text="#0f172a", muted="#64748b",
                  border="#e2e8f0", shadow="0 1px 3px rgba(15,23,42,.06), 0 4px 14px rgba(15,23,42,.04)",
                  side="#ffffff", accent="#4f46e5", grid="#eef2f7",
                  seq=["#4f46e5", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]),
    "Dark": dict(bg="#0b1220", card="#131c2f", text="#f1f5f9", muted="#94a3b8",
                 border="#233149", shadow="0 1px 3px rgba(0,0,0,.35), 0 6px 18px rgba(0,0,0,.25)",
                 side="#0e1627", accent="#818cf8", grid="#1f2b42",
                 seq=["#818cf8", "#22d3ee", "#34d399", "#fbbf24", "#f87171", "#a78bfa"]),
}

if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"

NAV = {
    "📈  Executive Overview": "Executive Overview",
    "👥  User Engagement": "User Engagement",
    "✅  Task Performance": "Task Performance",
    "🧩  Feature Usage": "Feature Usage",
    "🛡️  Data Quality": "Data Quality",
}

# ---------------- Sidebar (theme toggle first so CSS matches) ----------------
with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="logo">V</div><div><div class="brand-t">VELOOP</div>'
        '<div class="brand-s">Rewards Analytics</div></div></div>', unsafe_allow_html=True)
    st.radio("Appearance", ["Light", "Dark"], key="theme", horizontal=True)
    nav_label = st.radio("NAVIGATION", list(NAV.keys()), label_visibility="collapsed")
    st.markdown(
        '<div class="side-foot"><b>Data source</b><br>Simulated datasets (processed CSV files)'
        '<br><br><b>Dashboard version</b><br>v2.0 · VELOOP Rewards Analytics · 2026</div>',
        unsafe_allow_html=True)

page = NAV[nav_label]
T = THEMES[st.session_state["theme"]]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {{ --bg:{T['bg']}; --card:{T['card']}; --text:{T['text']}; --muted:{T['muted']};
        --border:{T['border']}; --accent:{T['accent']}; --shadow:{T['shadow']}; }}
html, body, .stApp, [class*="css"] {{ font-family:'Inter',system-ui,sans-serif; }}
.stApp {{ background:var(--bg); color:var(--text); }}
header[data-testid="stHeader"] {{ background:transparent; }}
.block-container {{ padding:2rem 2.2rem 3rem; max-width:1400px; }}
h1,h2,h3,h4,p,span,label,li,div[data-testid="stMarkdownContainer"] {{ color:var(--text); }}
[data-testid="stSidebar"], [data-testid="stSidebar"]>div:first-child {{
    background:{T['side']} !important; border-right:1px solid var(--border); }}
[data-testid="stSidebar"] * {{ color:var(--text); }}
[data-testid="stSidebar"] [role="radiogroup"] label {{
    padding:.55rem .75rem; border-radius:10px; width:100%; margin-bottom:2px; cursor:pointer; }}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{ background:{T['grid']}; }}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
    background:{T['accent']}22; font-weight:600; }}
.brand {{ display:flex; gap:.7rem; align-items:center; margin:.2rem 0 1.2rem; }}
.logo {{ width:38px; height:38px; border-radius:11px; display:flex; align-items:center; justify-content:center;
        background:linear-gradient(135deg,{T['seq'][0]},{T['seq'][1]}); color:#fff !important; font-weight:700; font-size:1.2rem; }}
.brand-t {{ font-weight:700; letter-spacing:.08em; font-size:1.1rem; }}
.brand-s {{ color:var(--muted) !important; font-size:.78rem; }}
.side-foot {{ margin-top:1.5rem; padding-top:1rem; border-top:1px solid var(--border);
             font-size:.76rem; color:var(--muted) !important; line-height:1.5; }}
.side-foot * {{ color:var(--muted) !important; }}
.page-title {{ font-size:1.8rem; font-weight:700; margin:0; letter-spacing:-.02em; }}
.page-sub {{ color:var(--muted) !important; margin:.15rem 0 1.4rem; font-size:.95rem; }}
.kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin-bottom:18px; }}
.kpi {{ background:var(--card); border:1px solid var(--border); border-radius:14px; padding:16px 18px;
       box-shadow:var(--shadow); min-width:0; border-top:3px solid var(--accent); }}
.kpi-l {{ font-size:.74rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted) !important; font-weight:600; }}
.kpi-v {{ font-size:1.75rem; font-weight:700; margin-top:4px; line-height:1.15; overflow-wrap:anywhere; }}
.kpi-s {{ font-size:.76rem; color:var(--muted) !important; margin-top:2px; }}
.sec {{ font-size:1.05rem; font-weight:600; margin:1.2rem 0 .5rem; }}
.note {{ background:var(--card); border:1px solid var(--border); border-left:4px solid var(--accent);
        border-radius:10px; padding:.8rem 1rem; font-size:.9rem; margin:.6rem 0; box-shadow:var(--shadow); }}
.note * {{ color:var(--text) !important; }}
[data-testid="stPlotlyChart"] {{ background:var(--card); border:1px solid var(--border); border-radius:14px;
        padding:6px; box-shadow:var(--shadow); width:100%; overflow:hidden; }}
[data-testid="stDataFrame"] {{ border:1px solid var(--border); border-radius:12px; overflow:hidden; width:100%; }}
.tbl-wrap {{ background:var(--card); border:1px solid var(--border); border-radius:12px; overflow:auto;
            max-height:480px; box-shadow:var(--shadow); width:100%; }}
.vt {{ width:100%; border-collapse:collapse; font-size:.86rem; }}
.vt th {{ position:sticky; top:0; background:var(--card); color:var(--muted) !important; text-align:left;
         padding:10px 14px; font-weight:600; font-size:.74rem; text-transform:uppercase;
         letter-spacing:.05em; border-bottom:1px solid var(--border); white-space:nowrap; }}
.vt td {{ padding:9px 14px; color:var(--text) !important; border-top:1px solid var(--border); }}
.vt tr:hover td {{ background:{T['grid']}; }}
hr {{ border-color:var(--border); }}
@media (max-width:992px) {{ .block-container {{ padding:1.4rem 1.2rem 2rem; }} }}
@media (max-width:768px) {{
  .block-container {{ padding:1rem .75rem 2rem; }}
  .page-title {{ font-size:1.4rem; }}
  .kpi-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }}
  .kpi {{ padding:12px; }} .kpi-v {{ font-size:1.3rem; }}
  [data-testid="stHorizontalBlock"] {{ flex-wrap:wrap; }}
  [data-testid="stColumn"] {{ min-width:100% !important; }}
}}
@media (max-width:420px) {{ .kpi-grid {{ grid-template-columns:1fr; }} }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# UI HELPERS
# ============================================================
def header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div><div class="page-sub">{subtitle}</div>',
                unsafe_allow_html=True)


def kpis(items):
    html = "".join(
        f'<div class="kpi"><div class="kpi-l">{l}</div><div class="kpi-v">{v}</div>'
        f'{f"<div class=kpi-s>{s}</div>" if s else ""}</div>' for l, v, s in items)
    st.markdown(f'<div class="kpi-grid">{html}</div>', unsafe_allow_html=True)


def section(text):
    st.markdown(f'<div class="sec">{text}</div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)


def style(fig, height=340, legend=False):
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=T["text"], size=12),
        showlegend=legend, colorway=T["seq"], hoverlabel=dict(font_size=12),
        legend=dict(orientation="h", y=-0.15),
    )
    ax = dict(gridcolor=T["grid"], linecolor=T["border"], title=None, automargin=True,
              tickfont=dict(color=T["text"]), zerolinecolor=T["grid"])
    fig.update_xaxes(**ax)
    fig.update_yaxes(**ax)
    fig.update_layout(legend_font_color=T["text"])
    return fig


def _stretch(fn, *a, **kw):
    """Use the new width='stretch' API, falling back for older Streamlit."""
    try:
        return fn(*a, width="stretch", **kw)
    except TypeError:
        return fn(*a, use_container_width=True, **kw)


def show(fig):
    _stretch(st.plotly_chart, fig, theme=None, config={"displaylogo": False})


def line(series, name="Value", height=320):
    df = series.reset_index()
    df.columns = ["x", name]
    fig = px.line(df, x="x", y=name, markers=len(df) < 40)
    fig.update_traces(line=dict(width=2.5, color=T["seq"][0]), fill="tozeroy",
                      fillcolor=T["seq"][0] + "1f")
    return style(fig, height)


def bar(series, name="Value", horizontal=False, height=340):
    df = series.reset_index()
    df.columns = ["label", name]
    if horizontal:
        df = df.sort_values(name)
        fig = px.bar(df, x=name, y="label", orientation="h", text=name)
    else:
        fig = px.bar(df, x="label", y=name, text=name)
    fig.update_traces(marker_color=T["seq"][0], texttemplate="%{text:,}", textposition="outside",
                      cliponaxis=False, marker_cornerradius=6)
    return style(fig, height)


def donut(series, height=340):
    df = series.reset_index()
    df.columns = ["label", "count"]
    fig = px.pie(df, names="label", values="count", hole=0.62, color_discrete_sequence=T["seq"])
    fig.update_traces(textinfo="percent", marker=dict(line=dict(color=T["card"], width=2)))
    return style(fig, height, legend=True)


def table(df, **kw):
    html = df.to_html(index=False, border=0, classes="vt", escape=True).replace("\n", "")
    st.markdown(f'<div class="tbl-wrap">{html}</div>', unsafe_allow_html=True)


def has(df, *cols):
    return (not df.empty) and all(c in df.columns for c in cols)


def missing_data(msg="Required dataset or columns are not available."):
    note(f"⚠️ {msg}")


# ============================================================
# PAGES
# ============================================================
if page == "Executive Overview":
    header("Executive Overview", "Platform performance at a glance")

    total_users = users["user_id"].nunique() if not users.empty else 0
    active_users = daily["user_id"].nunique() if not daily.empty else 0
    total_sessions = sessions["session_id"].nunique() if not sessions.empty else 0
    total_events = events["event_id"].nunique() if not events.empty else 0
    avg_duration = sessions["session_duration_seconds"].mean() / 60 if not sessions.empty else 0

    kpis([
        ("Total Users", f"{total_users:,}", None),
        ("Active Users", f"{active_users:,}", "Users with daily activity"),
        ("Total Sessions", f"{total_sessions:,}", None),
        ("Total Events", f"{total_events:,}", None),
        ("Avg. Raw Session Duration", f"{avg_duration:.2f} min", "From raw sessions"),
        ("Available Features", f"{len(features):,}", None),
    ])

    c1, c2 = st.columns(2)
    with c1:
        section("Daily Active Users")
        if has(daily, "activity_date", "user_id"):
            show(line(daily.groupby("activity_date")["user_id"].nunique(), "Active users"))
    with c2:
        section("Task Status Distribution")
        if has(tasks, "task_status"):
            show(donut(tasks["task_status"].value_counts()))

    c3, c4 = st.columns(2)
    with c3:
        section("Top Features by Events")
        if has(features, "feature_name", "total_events"):
            top = features.sort_values("total_events", ascending=False).head(8)
            show(bar(top.set_index("feature_name")["total_events"], "Events", horizontal=True))
    with c4:
        section("Sessions by Status")
        if has(sessions, "session_status"):
            show(donut(sessions["session_status"].value_counts()))

    section("Insights")
    if has(tasks, "task_status"):
        rate = (tasks["task_status"] == "Completed").mean() * 100
        note(f"Overall task completion rate is <b>{rate:.1f}%</b> across {len(tasks):,} task records.")
    if has(features, "feature_name", "total_events"):
        tf = features.sort_values("total_events", ascending=False).iloc[0]
        note(f"Most used feature: <b>{tf['feature_name']}</b> with {int(tf['total_events']):,} events.")
    if has(daily, "activity_date", "user_id"):
        d = daily.groupby("activity_date")["user_id"].nunique()
        note(f"Peak daily active users: <b>{int(d.max()):,}</b> on <b>{d.idxmax()}</b>.")

    section("Dataset Snapshot")
    snap = pd.DataFrame([
        {"Dataset": n, "Rows": len(df), "Columns": len(df.columns)}
        for n, df in {"Users": users, "Daily Activity": daily, "Sessions": sessions,
                      "Task Activity": tasks, "Feature Events": events,
                      "Feature Usage": features, "Milestones": milestones}.items()])
    table(snap)

    note("Rewards, Wallet, Withdrawals and Referral analytics are pending because their "
         "datasets are not currently available.")

elif page == "User Engagement":
    header("User Engagement", "Analyze daily user activity and session behaviour")

    if not has(daily_activity, "activity_date", "user_id", "session_duration_minutes", "event_count"):
        missing_data("daily_activity.csv not found or missing expected columns.")
    else:
        dau = daily_activity.groupby("activity_date")["user_id"].nunique()
        avg_duration = daily_activity["session_duration_minutes"].mean()
        active_days = daily_activity["activity_date"].nunique()
        total_events = daily_activity["event_count"].sum()
        avg_events = daily_activity["event_count"].mean()

        kpis([
            ("Daily Active Users (Average)", f"{round(dau.mean()):,}", None),
            ("Avg. Daily Session Duration", f"{avg_duration:.2f} min", None),
            ("Active Dates", f"{active_days:,}", None),
            ("Total User Events", f"{int(total_events):,}", None),
            ("Avg. Events per Active Day", f"{avg_events:.2f}", None),
        ])

        section("Daily Active Users Trend")
        show(line(dau, "Active users"))

        section("Daily Session Duration Trend")
        dur = daily_activity.groupby("activity_date")["session_duration_minutes"].mean()
        show(line(dur, "Avg. minutes"))

        section("Weekly Active Users Trend")
        wd = daily_activity.copy()
        wd["activity_date"] = pd.to_datetime(wd["activity_date"])
        wau = wd.groupby(wd["activity_date"].dt.to_period("W"))["user_id"].nunique()
        wau = wau.iloc[:-1]  # last (partial) week excluded, as in original logic
        wau.index = wau.index.astype(str)
        show(bar(wau, "Weekly active users"))
        note("The most recent (partial) week is excluded from the weekly trend.")

elif page == "Task Performance":
    header("Task Performance", "Task completion and failure analytics")

    if not has(tasks, "task_status"):
        missing_data("task_activity.csv not found or missing expected columns.")
    else:
        status_counts = tasks["task_status"].value_counts()
        total_tasks = len(tasks)
        completed = int(status_counts.get("Completed", 0))
        failed = int(status_counts.get("Failed", 0))
        abandoned = int(status_counts.get("Abandoned", 0))
        pending = int(status_counts.get("Pending", 0))
        completion_rate = (completed / total_tasks * 100) if total_tasks else 0

        kpis([
            ("Total Tasks", f"{total_tasks:,}", None),
            ("Completed Tasks", f"{completed:,}", None),
            ("Failed Tasks", f"{failed:,}", None),
            ("Abandoned Tasks", f"{abandoned:,}", None),
            ("Pending Tasks", f"{pending:,}", None),
            ("Completion Rate", f"{completion_rate:.1f}%", None),
        ])

        c1, c2 = st.columns(2)
        with c1:
            section("Task Status Distribution")
            show(bar(status_counts, "Tasks"))
        with c2:
            section("Task Failure Reasons")
            if "failure_reason" in tasks.columns:
                fr = tasks[tasks["task_status"] == "Failed"]["failure_reason"].value_counts()
                if fr.empty:
                    note("No failed tasks with a recorded failure reason.")
                else:
                    show(bar(fr, "Failed tasks", horizontal=True))
                    note("Failure reasons shown for tasks with status “Failed”.")

elif page == "Feature Usage":
    header("Feature Usage", "Analyze feature adoption and user activity")

    if not has(features, "feature_name", "total_events"):
        missing_data("feature_usage.csv not found or missing expected columns.")
    else:
        total_features = features["feature_name"].nunique()
        total_events = int(features["total_events"].sum())
        unique_users = events["user_id"].nunique() if has(events, "user_id") else 0
        ranked = features.sort_values("total_events", ascending=False)
        top_feature = ranked.iloc[0]["feature_name"]

        kpis([
            ("Available Features", f"{total_features:,}", None),
            ("Total Feature Events", f"{total_events:,}", None),
            ("Unique Users", f"{unique_users:,}", "From feature events"),
            ("Most Used Feature", str(top_feature), None),
        ])

        section("Feature Usage Ranking")
        show(bar(ranked.set_index("feature_name")["total_events"], "Total events",
                 horizontal=True, height=max(340, 28 * len(ranked) + 60)))

        if "unique_users" in features.columns:
            section("Unique Users by Feature")
            show(bar(features.sort_values("unique_users", ascending=False)
                     .set_index("feature_name")["unique_users"], "Unique users"))

        section("Feature Performance Table")
        table(ranked)
        note(f"Most used feature: <b>{top_feature}</b>")

elif page == "Data Quality":
    header("Data Quality", "Dataset profiling and data quality monitoring")

    datasets = {
        "Users": users, "Daily Activity": daily, "Sessions": sessions,
        "Task Activity": tasks, "Feature Events": events,
        "Feature Usage": features, "Milestones": milestones,
    }
    quality_df = pd.DataFrame([{
        "Dataset": n, "Rows": len(df), "Columns": len(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
    } for n, df in datasets.items()])

    kpis([
        ("Total Datasets", f"{len(datasets):,}", None),
        ("Total Records", f"{int(quality_df['Rows'].sum()):,}", None),
        ("Missing Values", f"{int(quality_df['Missing Values'].sum()):,}", None),
        ("Exact Duplicate Rows", f"{int(quality_df['Duplicate Rows'].sum()):,}", None),
    ])

    section("Dataset Quality Summary")
    table(quality_df)

    c1, c2 = st.columns(2)
    with c1:
        section("Missing Values by Dataset")
        mc = quality_df[quality_df["Missing Values"] > 0].set_index("Dataset")["Missing Values"]
        if mc.empty:
            note("✅ No missing values found.")
        else:
            show(bar(mc, "Missing values", horizontal=True))
    with c2:
        section("Missing Values by Column")
        details = [{"Dataset": n, "Column": c, "Missing Values": int(k)}
                   for n, df in datasets.items() for c, k in df.isnull().sum().items() if k > 0]
        if details:
            table(pd.DataFrame(details).sort_values("Missing Values", ascending=False))
        else:
            note("✅ All columns are complete.")

    section("Data Quality Findings")
    findings = pd.DataFrame([
        {"Finding": "Completed tasks exceed daily task count", "Affected Records": 423,
         "Status": "Open - Investigation Required"},
        {"Finding": "Daily task count differs from raw task activity", "Affected Records": 282,
         "Status": "Open - Definition Verification Required"},
        {"Finding": "Daily session duration exceeds raw session duration by more than expected",
         "Affected Records": 15, "Status": "Open - Investigation Required"},
        {"Finding": "Daily records unmatched using session start date", "Affected Records": 5,
         "Status": "Open - Date Attribution Verification"},
        {"Finding": "Event sequence non-increasing transitions", "Affected Records": 15556,
         "Status": "Open - Event Order Verification"},
    ])
    table(findings)
    note("Findings are based on simulated data audits. Affected record counts represent "
         "investigation results, not confirmed production defects. Missing values and "
         "duplicate rows above are calculated live from the processed CSV files.")
