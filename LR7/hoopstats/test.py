import pandas as pd
import hoopstatsapp  # Import the entire module

# Sample DataFrame for testing
data = {
    'Player': ['John', 'Anna', 'John', 'Mike', None],
    'Points': [23, 12, 23, 45, 30]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# Clean the DataFrame using the cleanStats function
df_cleaned = hoopstatsapp.cleanStats(df)
print("\nCleaned DataFrame:")
print(df_cleaned)



