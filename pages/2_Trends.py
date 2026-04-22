import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
from utils.theme import apply_theme, apply_plotly_theme

st.set_page_config(layout="wide", page_title="FitSync · Trends & Insights")

# Apply theme (CSS + toggle button)
apply_theme()

# ── Page Content ──────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.title("Trends & Insights")

st.markdown(
    "<p style='font-size:1rem; margin-top:-8px; margin-bottom:24px; opacity:0.7;'>"
    "Explore distributions and monthly patterns in your health data."
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
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2,
)

if time_range == "Last 7 Days":
    date_threshold = df['date'].max() - pd.Timedelta(days=7)
    filtered_df = df[df['date'] > date_threshold]
elif time_range == "Last 30 Days":
    date_threshold = df['date'].max() - pd.Timedelta(days=30)
    filtered_df = df[df['date'] > date_threshold]
else:
    filtered_df = df

# ── Summary Statistics ────────────────────────────────────────────────────────
st.subheader("Summary Statistics")
st.dataframe(
    filtered_df[['recovery_score', 'sleep_hours', 'steps', 'calories_burned']].describe(),
    use_container_width=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Monthly Average Recovery ──────────────────────────────────────────────────
filtered_df['Month'] = filtered_df['date'].dt.to_period('M')
monthly_avg_recovery = filtered_df.groupby('Month')['recovery_score'].mean().reset_index()
monthly_avg_recovery['Month'] = monthly_avg_recovery['Month'].astype(str)

st.subheader("Average Recovery Score per Month")
line_chart_avg_recovery = px.line(
    monthly_avg_recovery,
    x='Month',
    y='recovery_score',
    title="Monthly Average Recovery Score",
    markers=True,
)
st.plotly_chart(apply_plotly_theme(line_chart_avg_recovery), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Histograms ────────────────────────────────────────────────────────────────
st.subheader("Distributions")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        apply_plotly_theme(px.histogram(filtered_df, x='steps', title="Distribution of Steps")),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        apply_plotly_theme(px.histogram(filtered_df, x='calories_burned', title="Distribution of Calories Burned")),
        use_container_width=True,
    )

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        apply_plotly_theme(px.histogram(filtered_df, x='recovery_score', title="Distribution of Recovery Score")),
        use_container_width=True,
    )

with col4:
    st.plotly_chart(
        apply_plotly_theme(px.histogram(filtered_df, x='sleep_hours', title="Distribution of Sleep Hours")),
        use_container_width=True,
    )