import pandas as pd

# creating the dataframe
physFrame = pd.read_csv('Phys221Lab01.csv')
print(physFrame.to_string())

editedPhysFrame = pd.read_csv('Phys221Lab01.csv')
# fills the empty columns of the Gravitational force column to be the mean gravitational force
editedPhysFrame['Gravitational Force'].fillna(editedPhysFrame['Gravitational Force'].mean(), inplace = True)

# fills the empty columns of the Coulomb's force column to be the median coulomb force
editedPhysFrame["Coulomb's Force"].fillna(editedPhysFrame["Coulomb's Force"].median(), inplace = True)
print(editedPhysFrame.to_string())

print()
# displays all the information for the first row
print(editedPhysFrame.loc[0])

