import pandas as pd

def cleanStats(df):
    """
    Cleans the DataFrame by:
    1. Dropping rows with missing values.
    2. Dropping duplicate rows.
    3. Stripping any leading or trailing spaces in column names.
    """
    df.dropna(inplace=True)  # Remove rows with missing data
    df.drop_duplicates(inplace=True)  # Remove duplicate rows
    df.columns = df.columns.str.strip()  # Clean column names
    return df
