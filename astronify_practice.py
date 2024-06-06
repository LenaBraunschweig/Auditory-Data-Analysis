# astronify practice
from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd

file_reader = pd.read_csv("data.csv")
x_axis = file_reader['Duration']
y_axis = file_reader['Pulse']

rows = len(x_axis)
columns = 2

data_table = Table(names = ('Duration', 'Pulse'))
for index in range(len(x_axis)):
  data_table.add_row(vals = (x_axis[index], y_axis[index]))


player = SoniSeries(data = data_table, time_col = 'Duration', val_col = 'Pulse')
player.sonify()
player.play()