# better astronify practice
from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd
import numpy

file_reader = pd.read_csv("random data.csv")
tbl = Table.from_pandas(file_reader)
#print(tbl.colnames)

x_vals = 'd (cm)'
y_vals = 'Difference'

# saving the file to a recording gets rid of the weird beeping noise
soni_phys = SoniSeries(tbl, time_col = x_vals, val_col = y_vals)
soni_phys.pitch_mapper.pitch_map_args['zero_point'] = file_reader.Difference.median()

soni_phys.sonify()
soni_phys.play()