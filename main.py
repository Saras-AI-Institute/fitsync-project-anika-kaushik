import streamlit as st
from modules.processor import process_data
import pandas as pd

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Load and process the data
df = process_data()

# Add a sidebar header and time range filter
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Filter the DataFrame based on the time range
if time_range == "Last 7 Days":
    date_threshold = df['Date'].max() - pd.Timedelta(days=7)
    filtered_df = df[df['Date'] > date_threshold]
elif time_range == "Last 30 Days":
    date_threshold = df['Date'].max() - pd.Timedelta(days=30)
    filtered_df = df[df['Date'] > date_threshold]
else:
    filtered_df = df

# Calculate metrics from the filtered data
avg_steps = filtered_df['steps'].mean()
avg_sleep_hours = filtered_df['sleep_hours'].mean()
avg_recovery_score = filtered_df['Recovery_Score'].mean()

# Create a 3-column layout
col1, col2, col3 = st.columns(3)
# Display filtered metrics in columns
with col1:
    st.metric(label="Average Steps", value=f"{avg_steps:.0f}", delta=None)

with col2:
    st.metric(label="Average Sleep Hours", value=f"{avg_sleep_hours:.1f}", delta=None)

with col3:
    st.metric(label="Average Recovery Score", value=f"{avg_recovery_score:.1f}", delta=None)

# Display the processed DataFrame
st.write("### Processed Health Data")
st.dataframe(filtered_df)

# Additional components can be added here for further interaction and visualization
# e.g., charts, filters, etc.