from modules.processor import load_data, calculate_recovery_score

df = load_data()
print("Columns in DataFrame:", df.columns)  # Verify column names
df = calculate_recovery_score(df)


print(df[['date', 'sleep_hours', 'heart_rate_bpm', 'Recovery_Score']].head(10))

# ... existing code ...', 'Heart_Rate_bpm', 'Recovery_Score']].head(10))