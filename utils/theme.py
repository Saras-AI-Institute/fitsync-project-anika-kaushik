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
            "primary": "#7A1A00",
            "secondary": "#A83200",
            "accent": "#C84B00",
            "bg": "#F0E4CF",
            "paper_bg": "#F7F1E8",
            "font_color": "#1A0A00",
            "grid_color": "#B89A6A",
            "tick_color": "#3B2A1A",
            "axis_color": "#5C3D2A",
        }


def _fmt_cell(val):
    """Format a cell value cleanly for HTML display."""
    import pandas as pd
    import numpy as np

    if val is None:
        return ""
    # Datetime / Timestamp → date only (covers pd.Timestamp and np.datetime64)
    if isinstance(val, pd.Timestamp):
        return val.strftime("%Y-%m-%d")
    try:
        if isinstance(val, np.datetime64):
            return pd.Timestamp(val).strftime("%Y-%m-%d")
    except Exception:
        pass
    # Try datetime string cleanup (e.g. "2025-01-01 00:00:00")
    if isinstance(val, str) and " 00:00:00" in val:
        return val.replace(" 00:00:00", "")
    # Numpy float → treat as float
    if isinstance(val, (float, np.floating)):
        if val == int(val):
            return f"{int(val):,}"
        return f"{val:,.2f}"
    # Numpy int → treat as int
    if isinstance(val, (int, np.integer)):
        return f"{val:,}"
    return str(val)


def themed_dataframe(df):
    """
    Render a DataFrame in a way that respects the current theme.

    - Dark mode  → st.dataframe() (native, looks great on dark bg)
    - Light mode → custom HTML table (iframe-based st.dataframe cannot be
                   styled from the outside, so text is invisible on light bg)
    """
    import pandas as pd

    if st.session_state.get('theme', 'dark') == 'dark':
        st.dataframe(df, use_container_width=True)
        return

    c = get_chart_colors()
    # Extract to plain variables — backslashes inside f-string expressions are
    # a SyntaxError in Python < 3.12, so we avoid them entirely.
    font_color = c["font_color"]
    grid_color = c["grid_color"]
    bg         = c["bg"]
    paper_bg   = c["paper_bg"]

    # Inject a scoped CSS rule so Streamlit's own global overrides can't win
    st.markdown(
        f"""
        <style>
        .fitsync-table th {{
            padding: 10px 16px !important;
            text-align: left !important;
            font-weight: 600 !important;
            font-size: 12px !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: {font_color} !important;
            border-bottom: 2px solid {grid_color} !important;
            white-space: nowrap !important;
            background: {paper_bg} !important;
        }}
        .fitsync-table td {{
            padding: 9px 16px !important;
            color: {font_color} !important;
            font-size: 13px !important;
            border-bottom: 1px solid {grid_color} !important;
            white-space: nowrap !important;
        }}
        .fitsync-table tr:nth-child(even) {{ background: {paper_bg} !important; }}
        .fitsync-table tr:nth-child(odd)  {{ background: {bg} !important; }}
        .fitsync-table tr:hover {{ background: {grid_color} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Build headers
    idx_header = "<th>#</th>"
    headers = "".join(f"<th>{col}</th>" for col in df.columns)

    # Build rows
    rows_html = ""
    for i, (idx, row) in enumerate(df.iterrows()):
        if isinstance(idx, pd.Timestamp):
            idx_display = idx.strftime("%Y-%m-%d")
        else:
            idx_display = str(idx)
        idx_cell = f"<td style='opacity:0.6;'>{idx_display}</td>"
        cells = "".join(f"<td>{_fmt_cell(val)}</td>" for val in row)
        rows_html += f"<tr>{idx_cell}{cells}</tr>"

    html = f"""
    <div style="overflow-x:auto; overflow-y:auto; max-height:400px; border-radius:10px;
                border:1px solid {grid_color}; margin-bottom:8px;">
      <table class='fitsync-table' style="width:100%; border-collapse:collapse;
             font-family:'Lato',sans-serif; background:{bg};">
        <thead style="position:sticky; top:0; z-index:1;">
          <tr>{idx_header}{headers}</tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def apply_plotly_theme(fig):
    """Apply the current FitSync theme to a Plotly figure in-place and return it."""
    c = get_chart_colors()
    tmpl = "plotly_dark" if st.session_state.get("theme", "dark") == "dark" else "none"
    axis_style = dict(
        gridcolor=c["grid_color"],
        zerolinecolor=c["grid_color"],
        tickfont=dict(color=c["font_color"]),
        titlefont=dict(color=c["font_color"]),
        linecolor=c["grid_color"],
        tickcolor=c["font_color"],
    )
    fig.update_layout(
        template=tmpl,
        plot_bgcolor=c["bg"],
        paper_bgcolor=c["paper_bg"],
        font=dict(color=c["font_color"], family="Lato, sans-serif"),
        font_color=c["font_color"],
        title_font_color=c["font_color"],
        legend=dict(
            font=dict(color=c["font_color"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=axis_style,
        yaxis=axis_style,
        coloraxis_colorbar=dict(
            tickfont=dict(color=c["font_color"]),
            titlefont=dict(color=c["font_color"]),
        ),
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
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

        /* ── Sidebar nav gradient fade fix ── */
        [data-testid="stSidebarNav"] > div:not(ul) {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
        }
        [data-testid="stSidebarNav"] div[style*="position: absolute"],
        [data-testid="stSidebarNav"] div[style*="position:absolute"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] > div {
            display: none !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] > div:has(ul) {
            display: block !important;
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
        h1, h2, h3, h4, h5, h6 { color: #6B1200 !important; }
        p, li, span, div, label { color: #3B2A1A !important; }

        [data-testid="metric-container"] {
            background-color: #F0E4CF !important;
            box-shadow: 0 4px 18px rgba(107,18,0,0.10) !important;
        }
        [data-testid="metric-container"] label { color: #7A3010 !important; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #6B1200 !important; }
        hr { background-color: #C8A882 !important; }

        h2::before {
            content: '';
            display: inline-block;
            width: 4px; height: 1em;
            background: #8B1A00;
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

        /* ── FIX: Selectbox trigger box ── */
        .stSelectbox > div > div,
        [data-baseweb="select"] > div,
        [data-baseweb="select"] {
            background-color: #EDE4D3 !important;
            border-color: #C8A882 !important;
            color: #3B2A1A !important;
        }
        [data-baseweb="select"] span,
        [data-baseweb="select"] div {
            color: #3B2A1A !important;
            background-color: transparent !important;
        }

        /* ── FIX: Selectbox dropdown popup (the dark popover) ── */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        ul[data-baseweb="menu"],
        [role="listbox"],
        [data-baseweb="popover"] > div,
        [data-baseweb="popover"] [role="option"] {
            background-color: #F0E4CF !important;
            border-color: #C8A882 !important;
            color: #3B2A1A !important;
        }
        [data-baseweb="popover"] li,
        [data-baseweb="menu"] li,
        [role="option"] {
            background-color: #F0E4CF !important;
            color: #3B2A1A !important;
        }
        [data-baseweb="popover"] li:hover,
        [data-baseweb="menu"] li:hover,
        [role="option"]:hover {
            background-color: #E0D0B5 !important;
            color: #6B1200 !important;
        }
        /* Selected item highlight */
        [aria-selected="true"] {
            background-color: #DDD0B8 !important;
            color: #6B1200 !important;
        }

        /* ── FIX: Number input boxes (sidebar + main) ── */
        input[type="number"],
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input,
        .stNumberInput input {
            background-color: #EDE4D3 !important;
            color: #3B2A1A !important;
            border-color: #C8A882 !important;
        }
        [data-baseweb="input"],
        [data-baseweb="base-input"],
        .stNumberInput > div {
            background-color: #EDE4D3 !important;
            border-color: #C8A882 !important;
        }
        /* Number input +/- step buttons */
        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"],
        .stNumberInput button {
            background-color: #DDD0B8 !important;
            color: #6B1200 !important;
            border-color: #C8A882 !important;
        }
        .stNumberInput button:hover {
            background-color: #C8A882 !important;
        }

        /* ── FIX: Text inputs & date pickers ── */
        input[type="text"],
        input[type="date"],
        textarea {
            background-color: #EDE4D3 !important;
            color: #3B2A1A !important;
            border-color: #C8A882 !important;
        }

        /* ── FIX: Dataframe / table ── */
        [data-testid="stDataFrame"],
        .stDataFrame,
        iframe[title="st_dataframe"],
        .glideDataEditor,
        .dvn-scroller {
            background-color: #F0E4CF !important;
            color: #3B2A1A !important;
        }
        /* Arrow table cells */
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrame"] td,
        [data-testid="stDataFrameResizable"] th,
        [data-testid="stDataFrameResizable"] td {
            background-color: #F0E4CF !important;
            color: #3B2A1A !important;
            border-color: #C8A882 !important;
        }
        /* The inner iframe Streamlit uses for dataframes needs a white bg
           so the GlideDataGrid picks up light colours. We set it via the
           CSS custom property Streamlit exposes. */
        [data-testid="stDataFrame"] > div {
            --background-color: #F0E4CF;
            background-color: #F0E4CF !important;
        }

        /* ── FIX: Multiselect tags ── */
        [data-baseweb="tag"] {
            background-color: #DDD0B8 !important;
            color: #6B1200 !important;
        }

        /* ── FIX: Slider ── */
        [data-baseweb="slider"] [role="slider"] {
            background-color: #8B1A00 !important;
        }

        /* ── FIX: Sidebar number inputs specifically ── */
        section[data-testid="stSidebar"] input[type="number"],
        section[data-testid="stSidebar"] [data-baseweb="input"] input,
        section[data-testid="stSidebar"] [data-baseweb="base-input"] {
            background-color: #E0D0B5 !important;
            color: #3B2A1A !important;
            border-color: #B89A6A !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="input"],
        section[data-testid="stSidebar"] [data-baseweb="base-input"] {
            background-color: #E0D0B5 !important;
            border-color: #B89A6A !important;
        }
        section[data-testid="stSidebar"] [data-testid="stNumberInputStepDown"],
        section[data-testid="stSidebar"] [data-testid="stNumberInputStepUp"] {
            background-color: #D0C0A0 !important;
            color: #6B1200 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )