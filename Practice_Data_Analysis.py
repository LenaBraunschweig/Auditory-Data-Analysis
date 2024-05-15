import pandas as pd
import matplotlib.pyplot as plt


# general practice
'''df = pd.read_csv('Data.csv')
df.drop_duplicates(inplace = True)
print(df)

print(df.info())
print(df.corr())'''



# physics lab 1 reading
physFrame = pd.read_csv('Phys221Lab01.csv')
print(physFrame.to_string())