#VANCE DAVID G. SAMIA
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "breadprice.csv"
df = pd.read_csv(file_path)

# Compute the average price per year 
df["Average Price"] = df.iloc[:, 1:].mean(axis=1)

# Keep  "Year" and "Average Price" columns
df = df[["Year", "Average Price"]]

# Display the first few rows to verify
print(df.head())

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df["Year"], df["Average Price"], marker="o", linestyle="-", color="b", label="Bread Price")
plt.xlabel("Year")
plt.ylabel("Average Price ($)")
plt.title("Average Price of Bread Over the Years")
plt.legend()
plt.grid(True)
plt.show()
