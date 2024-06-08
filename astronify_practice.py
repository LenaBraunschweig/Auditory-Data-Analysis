# astronify practice
from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd

file_reader = pd.read_csv("PhysLab01.csv")
x_name = 'R'
y_name = 'Theta'

x_axis = file_reader[x_name]
y_axis = file_reader[y_name]

rows = len(x_axis)
columns = 2

data_table = Table(names = (x_name, y_name))
for index in range(len(x_axis)):
  data_table.add_row(vals = (x_axis[index], y_axis[index]))

player = SoniSeries(data = data_table, time_col = x_name, val_col = y_name)

player.sonify()
player.play()