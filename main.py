from utils.theme import apply_theme

import streamlit as st

st.set_page_config(layout="wide", page_title="FitSync")

# Apply theme (injects CSS + renders toggle button)
apply_theme()

# ── Page Content ──────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)  # breathing room below toggle

st.title("Welcome to FitSync")

st.markdown(
    """
    <p style="font-size:1.15rem; margin-top: -8px; margin-bottom: 28px;">
        Your personal health analytics dashboard
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Dashboard")
    st.write("View real-time metrics — steps, sleep, recovery score, and calories at a glance.")

with col2:
    st.markdown("### 📈 Trends")
    st.write("Explore monthly trends and distributions to understand your long-term health patterns.")

with col3:
    st.markdown("### 🔍 Insights")
    st.write("Discover correlations between your habits and performance through interactive charts.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; font-size:0.9rem; opacity:0.55;'>Use the sidebar to navigate between pages</p>",
    unsafe_allow_html=True,
)