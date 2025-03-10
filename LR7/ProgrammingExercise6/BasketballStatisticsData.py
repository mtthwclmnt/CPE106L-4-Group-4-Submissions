# DYTIANQUIN, CHALZEA FRANSEN C.
import pandas as pd

#Load the dataset
file_path = "cleanbrogdonstats.csv"
df = pd.read_csv(file_path)

def split_makes_attempts(column):
    makes = []
    attempts = []
    for value in column:
        make, attempt = map(int, value.split('-'))
        makes.append(make)
        attempts.append(attempt)
    return makes, attempts

data['3PTM'], data['3PTA'] = split_makes_attempts(data['3PT']) 
data['FTM'], data['FTA'] = split_makes_attempts(data['FT'])
data['FTM%'] = (data['FTM'] / data['FTA']) * 100
data['AFTM'] = data['FTA'] 

# Remove the FG, 3PT, and FT columns
data.drop(columns=['FG', '3PT', 'FT'], inplace=True)

# Reorder the columns
data = data[['MIN', '3PTM', '3PTA', 'FTM', 'FTA', 'FTM%', 'AFTM', 
             'FG%', '3P%', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS']]

# Display a header and print the updated DataFrame
print("Analyzing Basketball Statistics Data Set:")
print(data)
