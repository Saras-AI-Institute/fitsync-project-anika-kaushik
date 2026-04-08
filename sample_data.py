import pandas as pd

# Load the CSV file
data = pd.read_csv('data/health_data.csv')

# Print the first 5 rows
print("First 5 rows:")
print(data.head())

# Print the number of missing values in each column
print("\nNumber of missing values in each column:")
print(data.isnull().sum())