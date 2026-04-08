import pandas as pd
from datetime import datetime


def load_data():
    """
    Load and clean the health data from CSV.

    This function:
    - Reads data from 'data/health_data.csv'.
    - Fills missing 'Steps' with the median value.
    - Fills missing 'Sleep_Hour' with 7.0.
    - Fills missing 'Heart_Rate_bpm' with 68.
    - Fills other missing values with their column median.
    - Converts 'Date' column to datetime objects.

    Returns:
        pd.DataFrame: A cleaned pandas DataFrame.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv('data/health_data.csv')

    # Fill missing values for specific columns
    if 'Steps' in df:
        df['Steps'].fillna(df['Steps'].median(), inplace=True)

    if 'Sleep_Hour' in df:
        df['Sleep_Hour'].fillna(7.0, inplace=True)

    if 'Heart_Rate_bpm' in df:
        df['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Fill any other numerical columns with the median of that column
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Convert 'Date' column to datetime objects
    if 'Date' in df:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    return df


def calculate_recovery_score(df):
    """
    Calculate and add 'Recovery_Score' to the DataFrame.

    The score is calculated based on:
    - Sleep_Hours: 7+ hours significantly improve the score, <6 is bad.
    - Heart_Rate_bpm: A lower heart rate is better.
    - Steps: Higher steps can indicate good activity but might slightly reduce recovery.

    Args:
        df (pd.DataFrame): DataFrame with necessary health data columns.
    """
    # Initialize Recovery_Score with a baseline of 50
    df['Recovery_Score'] = 50

    # Adjust score based on sleep_hours
    df.loc[df['sleep_hours'] >= 7, 'Recovery_Score'] += 20  # Good sleep
    df.loc[df['sleep_hours'] < 6, 'Recovery_Score'] -= 20  # Poor sleep

    # Adjust score based on heart_rate_bpm
    # Lower heart rate improves recovery
    df['Recovery_Score'] -= (df['heart_rate_bpm'] - 65) * 0.5

    # Adjust score based on steps
    # High steps may slightly decrease recovery due to potential strain
    df['Recovery_Score'] -= ((df['steps'] - 10000) / 1000) * 2

    # Ensure Recovery_Score stays between 0 and 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(lower=0, upper=100)

    return df


def process_data():
    """
    Process data by loading, calculating recovery score, and returning the processed DataFrame.

    Returns:
        pd.DataFrame: A processed pandas DataFrame with Recovery Score added.
    """
    # Load cleaned data
    df = load_data()

    # Calculate Recovery Score
    df = calculate_recovery_score(df)

    return df
