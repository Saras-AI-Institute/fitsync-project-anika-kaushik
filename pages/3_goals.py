import streamlit as st
from modules.processor import process_data
import pandas as pd
from utils.theme import apply_theme, get_chart_colors, apply_plotly_theme
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="FitSync · Goals")

apply_theme()

# ── Page Content ──────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.title("Goal Setter")

st.markdown(
    "<p style='font-size:1rem; margin-top:-8px; margin-bottom:24px; opacity:0.7;'>"
    "Set personal targets for steps, sleep, and recovery — then track your progress."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
df = process_data()
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'])

# ── Sidebar: Set Goals ────────────────────────────────────────────────────────
st.sidebar.header("Set Your Goals")

# Initialise defaults in session state once
if 'goal_steps' not in st.session_state:
    st.session_state['goal_steps'] = 8000
if 'goal_sleep' not in st.session_state:
    st.session_state['goal_sleep'] = 8.0
if 'goal_recovery' not in st.session_state:
    st.session_state['goal_recovery'] = 75

st.sidebar.markdown("**Daily Step Goal**")
goal_steps = st.sidebar.number_input(
    "Steps target",
    min_value=1000,
    max_value=30000,
    value=st.session_state['goal_steps'],
    step=500,
    key="goal_steps",
)

st.sidebar.markdown("**Sleep Goal (hours)**")
goal_sleep = st.sidebar.number_input(
    "Sleep target (hrs)",
    min_value=4.0,
    max_value=12.0,
    value=st.session_state['goal_sleep'],
    step=0.5,
    key="goal_sleep",
)

st.sidebar.markdown("**Recovery Score Goal**")
goal_recovery = st.sidebar.number_input(
    "Recovery score target",
    min_value=10,
    max_value=100,
    value=st.session_state['goal_recovery'],
    step=5,
    key="goal_recovery",
)

# ── Sidebar: Evaluation Window ────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown("**Evaluation Period**")
period = st.sidebar.selectbox(
    "Measure progress over",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=0,
)

if period == "Last 7 Days":
    threshold = df['date'].max() - pd.Timedelta(days=7)
    eval_df = df[df['date'] > threshold]
elif period == "Last 30 Days":
    threshold = df['date'].max() - pd.Timedelta(days=30)
    eval_df = df[df['date'] > threshold]
else:
    eval_df = df

# ── Compute Actuals ───────────────────────────────────────────────────────────
avg_steps   = eval_df['steps'].mean()          if len(eval_df) else 0
avg_sleep   = eval_df['sleep_hours'].mean()    if len(eval_df) else 0
avg_recovery = eval_df['recovery_score'].mean() if len(eval_df) else 0

pct_steps    = min(avg_steps    / goal_steps    * 100, 100)
pct_sleep    = min(avg_sleep    / goal_sleep    * 100, 100)
pct_recovery = min(avg_recovery / goal_recovery * 100, 100)

c = get_chart_colors()

def _status_emoji(pct: float) -> str:
    if pct >= 100: return "🏆"
    if pct >= 80:  return "🔥"
    if pct >= 50:  return "💪"
    return "📉"

def _progress_card(label: str, actual: float, goal: float, pct: float, unit: str = ""):
    bar_color_fill = c["primary"]
    bar_bg         = c["grid_color"]
    text_color     = c["font_color"]
    val_color      = c["secondary"]
    card_bg        = c["bg"]

    emoji = _status_emoji(pct)
    actual_fmt = f"{actual:,.0f}" if unit == "" else f"{actual:.1f}"
    goal_fmt   = f"{goal:,.0f}"   if unit == "" else f"{goal:.1f}"

    html = f"""
    <div class="goal-card" style="background:{card_bg};">
        <div class="goal-label" style="color:{text_color};">{label}</div>
        <div class="goal-values" style="color:{val_color};">
            {emoji} {actual_fmt}{unit}
            <span style="font-size:1rem; opacity:0.55;"> / {goal_fmt}{unit}</span>
        </div>
        <div class="goal-bar-bg" style="background:{bar_bg};">
            <div class="goal-bar-fill" style="width:{pct:.1f}%; background:linear-gradient(90deg,{bar_color_fill},{c['accent']});"></div>
        </div>
        <div class="goal-pct" style="color:{text_color};">{pct:.1f}% of goal achieved</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ── Goal Cards ────────────────────────────────────────────────────────────────
st.subheader(f"Progress Overview — {period}")
col1, col2, col3 = st.columns(3)

with col1:
    _progress_card("Daily Steps", avg_steps, goal_steps, pct_steps)

with col2:
    _progress_card("Sleep Hours", avg_sleep, goal_sleep, pct_sleep, unit=" hrs")

with col3:
    _progress_card("Recovery Score", avg_recovery, goal_recovery, pct_recovery)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Gauge Charts ──────────────────────────────────────────────────────────────
st.subheader("Goal Gauges")

def _gauge(title: str, value: float, goal: float, pct: float):
    color = c["primary"] if pct < 80 else ("#F5A623" if pct < 100 else "#27AE60")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={'reference': goal, 'valueformat': '.1f'},
        title={'text': title, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, goal * 1.2]},
            'bar': {'color': color},
            'bgcolor': c["bg"],
            'borderwidth': 1,
            'bordercolor': c["grid_color"],
            'steps': [
                {'range': [0, goal * 0.5],  'color': c["grid_color"]},
                {'range': [goal * 0.5, goal], 'color': c["bg"]},
            ],
            'threshold': {
                'line': {'color': c["accent"], 'width': 3},
                'thickness': 0.85,
                'value': goal,
            },
        },
        number={'font': {'color': c["font_color"]}},
    ))
    fig.update_layout(
        height=220,
        margin=dict(t=40, b=10, l=20, r=20),
    )
    return apply_plotly_theme(fig)

gc1, gc2, gc3 = st.columns(3)
with gc1:
    st.plotly_chart(_gauge("Steps", avg_steps, goal_steps, pct_steps), use_container_width=True)
with gc2:
    st.plotly_chart(_gauge("Sleep (hrs)", avg_sleep, goal_sleep, pct_sleep), use_container_width=True)
with gc3:
    st.plotly_chart(_gauge("Recovery Score", avg_recovery, goal_recovery, pct_recovery), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Day-by-day progress bars (vs goal) ────────────────────────────────────────
st.subheader("Daily Breakdown vs Goal")

metric_choice = st.selectbox(
    "Choose metric to inspect",
    options=["Steps", "Sleep Hours", "Recovery Score"],
)

col_map = {"Steps": ("steps", goal_steps), "Sleep Hours": ("sleep_hours", goal_sleep), "Recovery Score": ("recovery_score", goal_recovery)}
col_key, target = col_map[metric_choice]

plot_df = eval_df[['date', col_key]].copy()
plot_df['goal'] = target
plot_df['date_str'] = plot_df['date'].dt.strftime('%b %d')

import plotly.express as px
bar_fig = px.bar(
    plot_df,
    x='date_str',
    y=col_key,
    title=f"Daily {metric_choice} vs Target ({target:g})",
    labels={'date_str': 'Date', col_key: metric_choice},
)
bar_fig.add_hline(
    y=target,
    line_dash="dash",
    line_color=c["accent"],
    annotation_text="Goal",
    annotation_position="top right",
)
st.plotly_chart(apply_plotly_theme(bar_fig), use_container_width=True)

# ── Days Goal Met ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Goal Achievement Summary")

days_steps_met    = (eval_df['steps']          >= goal_steps).sum()
days_sleep_met    = (eval_df['sleep_hours']    >= goal_sleep).sum()
days_recovery_met = (eval_df['recovery_score'] >= goal_recovery).sum()
total_days        = len(eval_df)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Steps Goal Days Met",    f"{days_steps_met} / {total_days}",    f"{days_steps_met/total_days*100:.0f}%" if total_days else "N/A")
with m2:
    st.metric("Sleep Goal Days Met",    f"{days_sleep_met} / {total_days}",    f"{days_sleep_met/total_days*100:.0f}%" if total_days else "N/A")
with m3:
    st.metric("Recovery Goal Days Met", f"{days_recovery_met} / {total_days}", f"{days_recovery_met/total_days*100:.0f}%" if total_days else "N/A")