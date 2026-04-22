import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
from utils.theme import apply_theme, apply_plotly_theme

st.set_page_config(layout="wide", page_title="FitSync · Dashboard")

# Apply theme (CSS + toggle button)
apply_theme()

# ── Page Content ──────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.title("FitSync — Personal Health Analytics")

st.markdown(
    "<p style='font-size:1rem; margin-top:-8px; margin-bottom:24px; opacity:0.7;'>"
    "Track your recovery, sleep, and daily activity in one place."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
df = process_data()
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'])

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time", "Custom Range"],
    index=2,
)

# ── Date Range Picker (additive — only shown when "Custom Range" selected) ────
if time_range == "Custom Range":
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    st.sidebar.markdown("**Select Date Range**")
    date_from = st.sidebar.date_input(
        "From",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="date_from",
    )
    date_to = st.sidebar.date_input(
        "To",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="date_to",
    )

    # Guard: ensure from <= to
    if date_from > date_to:
        st.sidebar.warning("⚠️ 'From' date must be before 'To' date.")
        date_from, date_to = date_to, date_from

    filtered_df = df[
        (df['date'].dt.date >= date_from) &
        (df['date'].dt.date <= date_to)
    ]
    st.sidebar.caption(f"Showing {len(filtered_df)} records")

elif time_range == "Last 7 Days":
    date_threshold = df['date'].max() - pd.Timedelta(days=7)
    filtered_df = df[df['date'] > date_threshold]
elif time_range == "Last 30 Days":
    date_threshold = df['date'].max() - pd.Timedelta(days=30)
    filtered_df = df[df['date'] > date_threshold]
else:
    filtered_df = df

# ── KPI Metrics ───────────────────────────────────────────────────────────────
avg_steps = filtered_df['steps'].mean()
avg_sleep_hours = filtered_df['sleep_hours'].mean()
avg_recovery_score = filtered_df['recovery_score'].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Average Steps", value=f"{avg_steps:.0f}")
with col2:
    st.metric(label="Average Sleep Hours", value=f"{avg_sleep_hours:.1f}")
with col3:
    st.metric(label="Average Recovery Score", value=f"{avg_recovery_score:.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recovery Score & Sleep Trend")
    line_chart = px.line(
        filtered_df,
        x='date',
        y=['recovery_score', 'sleep_hours'],
        labels={'value': 'Measurement'},
        title="Recovery Score and Sleep Hours over Time",
    )
    st.plotly_chart(apply_plotly_theme(line_chart), use_container_width=True)

with col2:
    st.subheader("Recovery Score vs Daily Steps")
    scatter_plot = px.scatter(
        filtered_df,
        x='steps',
        y='recovery_score',
        color='sleep_hours',
        title="Scatter Plot: Recovery vs Steps",
        labels={'color': 'Sleep Hours'},
    )
    st.plotly_chart(apply_plotly_theme(scatter_plot), use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Recovery Score vs Resting Heart Rate")
    scatter_plot_hr = px.scatter(
        filtered_df,
        x='heart_rate_bpm',
        y='recovery_score',
        title="Scatter Plot: Recovery vs Heart Rate",
        labels={'x': 'Heart Rate (bpm)', 'y': 'Recovery Score'},
    )
    st.plotly_chart(apply_plotly_theme(scatter_plot_hr), use_container_width=True)

with col4:
    st.subheader("Daily Calories Burned Trend")
    line_chart_calories = px.line(
        filtered_df,
        x='date',
        y='calories_burned',
        title="Line Chart: Calories Burned",
    )
    st.plotly_chart(apply_plotly_theme(line_chart_calories), use_container_width=True)

# ── Data Table ────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Processed Health Data")
st.dataframe(filtered_df, use_container_width=True)