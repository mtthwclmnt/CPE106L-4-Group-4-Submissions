import pandas as pd
import matplotlib.pyplot as plt

# Function to clean the DataFrame
def cleanStats(df):
    # Strip whitespace from columns and player names
    df.columns = df.columns.str.strip()
    df['Player'] = df['Player'].str.strip()
    
    # Drop rows with any missing values
    df.dropna(inplace=True)
    
    # Save the cleaned data to a new CSV file
    df.to_csv('cleaned_hoopstats.csv', index=False)
    print("\n✅ Data cleaned and saved to: cleaned_hoopstats.csv\n")
    
    return df

# Function to generate a team summary
def teamSummary(df):
    summary = df.groupby('Team').agg({
        'Points': 'sum',
        'Assists': 'sum',
        'Rebounds': 'sum',
        'Player': lambda x: ', '.join(x)
    }).reset_index()
    
    # Save the team summary to a CSV file
    summary.to_csv('team_summary.csv', index=False)
    print("✅ Team summary saved to: team_summary.csv\n")
    
    # Clean output formatting for terminal
    print(" " * 25 + "==== TEAM SUMMARY ====")
    print()
    print(f"{'Team':<10}{'Player':<35}{'Points':<10}{'Assists':<10}{'Rebounds':<10}")
    print("-" * 75)
    for i, row in summary.iterrows():
        print(f"{row['Team']:<10}{row['Player']:<35}{row['Points']:<10}{row['Assists']:<10}{row['Rebounds']:<10}")

# Function to plot performance
def plot_performance(df):
    df.groupby('Team')['Points'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Points by Team')
    plt.ylabel('Points')
    plt.show()

# Main function
def main():
    # Load the data
    df = pd.read_csv('hoopstats.csv')
    
    # Clean the data
    cleaned_df = cleanStats(df)
    
    # Generate and display the team summary
    teamSummary(cleaned_df)
    
    # Plot the performance
    plot_performance(cleaned_df)

if __name__ == "__main__":
    main()


