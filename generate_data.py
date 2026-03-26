import pandas as pd
import numpy as np
from datetime import timedelta, date

# Generate date range for one year starting from 2025-01-01
start_date = date(2025, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Generate random data for each column
np.random.seed(42)  # For reproducibili

steps = np.random.normal(8500, 2000, 365).clip(3000, 18000)
sleep_hours = np.random.normal(7.2, 1, 365).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(68, 10, 365).clip(48, 110)
calories_burned = np.random.randint(1800, 4200, 365)
active_minutes = np.random.randint(20, 180, 365)

# Assemble into a DataFrame
health_data = pd.DataFrame({
    'date': dates,
    'steps': steps,
    'sleep_hours': sleep_hours,
    'heart_rate_bpm': heart_rate_bpm,
    'calories_burned': calories_burned,
    'active_minutes': active_minutes
})

# Introduce missing values at random positions (5% of each column)
for column in health_data.columns[1:]:  # Skip the date column
    health_data.loc[health_data.sample(frac=0.05).index, column] = np.nan

# Save to CSV
health_data.to_csv('data/health_data.csv', index=False)