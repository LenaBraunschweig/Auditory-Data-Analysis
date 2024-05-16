import pandas as pd

# comment: creating the dataframe
physFrame = pd.read_csv('Phys221Lab01.csv')
print(physFrame.to_string())

editedPhysFrame = pd.read_csv('Phys221Lab01.csv')
# comment: fills the empty columns of the Gravitational force column to be the mean gravitational force
editedPhysFrame.fillna({'Gravitational Force': editedPhysFrame['Gravitational Force'].mean()}, inplace = True)

# comment: fills the empty columns of the Coulomb's force column to be the median coulomb force
editedPhysFrame.fillna({"Colulomb's Force": editedPhysFrame["Coulomb's Force"].median()}, inplace = True)
print(editedPhysFrame.to_string())

print()
# comment: displays all the information for the first row
print(editedPhysFrame.loc[0])