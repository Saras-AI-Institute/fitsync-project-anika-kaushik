import pandas as pd


def load_data():
    """
    Load and clean the health data from a CSV file.

    This function reads data from 'data/health_data.csv', handles missing values,
    converts date strings to datetime objects, and returns a cleaned DataFrame.
    """
    # Read the CSV file
    data = pd.read_csv('data/health_data.csv')

    # Fill missing 'Steps' values with the median value of the column
    data['steps'].fillna(data['steps'].median(), inplace=True)

    # Fill missing 'Sleep_Hours' values with 7.0
    data['sleep_hours'].fillna(7.0, inplace=True)

    # Fill missing 'Heart_Rate_bpm' values with 68
    data['heart_rate_bpm'].fillna(68, inplace=True)

    # Fill missing values in other numerical columns with their median
    for column in data.select_dtypes(include=['float64', 'int64']).columns:
        if column not in ['steps', 'sleep_hours', 'heart_rate_bpm']:
            data[column].fillna(data[column].median(), inplace=True)

    # Convert the 'Date' column to datetime objects
    data['date'] = pd.to_datetime(data['date'])

    return data