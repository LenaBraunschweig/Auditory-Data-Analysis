import pandas as pd

# creates the dataframe
df = pd.read_csv('Data.csv')
df.drop_duplicates(inplace = True)
print(df)

# displays the info and correlations between the data
print(df.info())
print(df.corr())