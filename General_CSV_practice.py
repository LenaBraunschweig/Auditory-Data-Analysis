import pandas as pd

# general practice
df = pd.read_csv('Data.csv')
df.drop_duplicates(inplace = True)
print(df)

print(df.info())
print(df.corr())