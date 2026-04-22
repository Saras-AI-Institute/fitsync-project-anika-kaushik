import streamlit as st


# ── Chart theme helpers ────────────────────────────────────────────────────────

def get_chart_template():
    """Return the Plotly template name matching the current theme."""
    return "plotly_dark" if st.session_state.get('theme', 'dark') == 'dark' else "plotly_white"


def get_chart_colors():
    """Return a dict of chart accent colours for the current theme."""
    if st.session_state.get('theme', 'dark') == 'dark':
        return {
            "primary": "#4A7BF7",
            "secondary": "#A8C4FF",
            "accent": "#63B3ED",
            "bg": "#1C2333",
            "paper_bg": "#161B22",
            "font_color": "#C9D1D9",
            "grid_color": "#30363D",
        }
    else:
        return {
            "primary": "#7A1A00",      # darker rust
            "secondary": "#A83200",
            "accent": "#C84B00",
            "bg": "#F0E4CF",
            "paper_bg": "#F7F1E8",
            "font_color": "#3B2A1A",
            "grid_color": "#C8A882",
        }


def apply_plotly_theme(fig):
    """Apply the current FitSync theme to a Plotly figure in-place and return it."""
    c = get_chart_colors()
    tmpl = get_chart_template()
    fig.update_layout(
        template=tmpl,
        plot_bgcolor=c["bg"],
        paper_bgcolor=c["paper_bg"],
        font_color=c["font_color"],
        title_font_color=c["font_color"],
        legend_font_color=c["font_color"],
        xaxis=dict(gridcolor=c["grid_color"], zerolinecolor=c["grid_color"]),
        yaxis=dict(gridcolor=c["grid_color"], zerolinecolor=c["grid_color"]),
    )
    return fig


# ── Main entry point ───────────────────────────────────────────────────────────

def apply_theme():
    """Apply theme CSS and render the top-right toggle button."""
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'dark'

    _inject_base_css()

    if st.session_state['theme'] == 'dark':
        _apply_dark_mode()
    else:
        _apply_light_mode()

    _render_toggle_button()


def _render_toggle_button():
    label = "☀️ Light" if st.session_state['theme'] == 'dark' else "🌙 Dark"

    st.markdown(
        """
        <style>
        .theme-btn-container {
            position: fixed;
            top: 14px;
            right: 20px;
            z-index: 9999;
        }
        .theme-btn-container button {
            font-family: 'Georgia', serif !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            padding: 6px 16px !important;
            border-radius: 20px !important;
            border: 1.5px solid currentColor !important;
            cursor: pointer !important;
            transition: all 0.25s ease !important;
            letter-spacing: 0.03em !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    spacer, btn_col = st.columns([10, 1.2])
    with btn_col:
        if st.button(label, key="theme_toggle_btn"):
            st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
            st.rerun()


def _inject_base_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Lato', sans-serif !important;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="metric-container"] {
            border-radius: 12px !important;
            padding: 18px 22px !important;
            border: 1px solid rgba(128,128,128,0.15) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
        }
        [data-testid="metric-container"] label {
            font-family: 'Lato', sans-serif !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-family: 'Playfair Display', serif !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,0.12) !important;
        }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] h2 {
            font-family: 'Lato', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            font-size: 11px !important;
        }

        hr {
            border: none !important;
            height: 1px !important;
            opacity: 0.2 !important;
        }

        .stDataFrame {
            border-radius: 10px !important;
            overflow: hidden !important;
        }

        /* Goal setter progress bar */
        .goal-card {
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 16px;
            border: 1px solid rgba(128,128,128,0.15);
            transition: transform 0.2s ease;
        }
        .goal-card:hover { transform: translateY(-2px); }
        .goal-label {
            font-family: 'Lato', sans-serif;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .goal-values {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .goal-bar-bg {
            border-radius: 99px;
            height: 10px;
            width: 100%;
            overflow: hidden;
        }
        .goal-bar-fill {
            border-radius: 99px;
            height: 10px;
            transition: width 0.6s ease;
        }
        .goal-pct {
            font-family: 'Lato', sans-serif;
            font-size: 12px;
            margin-top: 6px;
            opacity: 0.75;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _apply_dark_mode():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"], .stApp {
            background-color: #0D1117 !important;
            color: #E8EAF0 !important;
        }
        section[data-testid="stSidebar"] { background-color: #161B22 !important; }
        section[data-testid="stSidebar"] * { color: #C9D1D9 !important; }
        h1, h2, h3, h4, h5, h6 { color: #F0F2F8 !important; }
        p, li, span, div, label { color: #C9D1D9 !important; }
        [data-testid="metric-container"] {
            background-color: #1C2333 !important;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
        }
        [data-testid="metric-container"] label { color: #8B9DC3 !important; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #A8C4FF !important; }
        hr { background-color: #30363D !important; }
        .stSelectbox > div > div {
            background-color: #1C2333 !important;
            border-color: #30363D !important;
            color: #E8EAF0 !important;
        }
        h2::before {
            content: '';
            display: inline-block;
            width: 4px; height: 1em;
            background: #4A7BF7;
            border-radius: 2px;
            margin-right: 10px;
            vertical-align: middle;
        }
        button[kind="secondary"] {
            background-color: #1C2333 !important;
            color: #A8C4FF !important;
            border-color: #4A7BF7 !important;
        }
        .goal-card { background-color: #1C2333; }
        .goal-label { color: #8B9DC3; }
        .goal-values { color: #A8C4FF; }
        .goal-bar-bg { background: #30363D; }
        .goal-bar-fill { background: linear-gradient(90deg, #4A7BF7, #63B3ED); }
        .goal-pct { color: #C9D1D9; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _apply_light_mode():
    st.markdown(
        """
        <style>
        /* ── LIGHT MODE (Beige & Darker Rust) ── */
        [data-testid="stAppViewContainer"], .stApp {
            background-color: #F7F1E8 !important;
            color: #3B2A1A !important;
        }
        section[data-testid="stSidebar"] { background-color: #EDE4D3 !important; }
        section[data-testid="stSidebar"] * { color: #5C3D2A !important; }
        h1, h2, h3, h4, h5, h6 { color: #6B1200 !important; }   /* darker rust */
        p, li, span, div, label { color: #3B2A1A !important; }
        [data-testid="metric-container"] {
            background-color: #F0E4CF !important;
            box-shadow: 0 4px 18px rgba(107,18,0,0.10) !important;
        }
        [data-testid="metric-container"] label { color: #7A3010 !important; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #6B1200 !important; }
        hr { background-color: #C8A882 !important; }
        .stSelectbox > div > div {
            background-color: #EDE4D3 !important;
            border-color: #C8A882 !important;
            color: #3B2A1A !important;
        }
        h2::before {
            content: '';
            display: inline-block;
            width: 4px; height: 1em;
            background: #8B1A00;        /* darker rust accent bar */
            border-radius: 2px;
            margin-right: 10px;
            vertical-align: middle;
        }
        button[kind="secondary"] {
            background-color: #EDE4D3 !important;
            color: #6B1200 !important;
            border-color: #8B1A00 !important;
        }
        .stApp p { color: #6B4226 !important; }
        .goal-card { background-color: #F0E4CF; }
        .goal-label { color: #7A3010; }
        .goal-values { color: #6B1200; }
        .goal-bar-bg { background: #DDD0B8; }
        .goal-bar-fill { background: linear-gradient(90deg, #8B1A00, #C84B00); }
        .goal-pct { color: #6B4226; }
        </style>
        """,
        unsafe_allow_html=True,
    )