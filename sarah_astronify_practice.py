from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd
import numpy

url = 'https://github.com/sgkane/sonification_tutorial_two/blob/main/weather_data.csv?raw=true'
df = pd.read_csv(url, index_col = 0)
'''print(df.columns)
print(df.shape) # returns the number of rows, columns as a tuple
print(df.iloc[-1]) # returns all the items in the last row'''

df.philadelphia_temp.median() # provides the median of the philadelphia temp column
df['timestep'] = pd.RangeIndex(0, len(df), step = 1)
tbl = Table.from_pandas(df)
# print(tbl.colnames) # tells the columns of the table
soni_philadelphia = SoniSeries(tbl, time_col = 'timestep', val_col = 'philadelphia_temp')
soni_philadelphia.sonify()
#soni_philadelphia.write("Philadelphia_data.wav")


soni_delhi = SoniSeries(tbl, timecol = 'timestep', val_col = 'delhi_temp')
soni_delhi.pitch_mapper.pitch_map_args['zero_point'] = df.philadelphia_temp.median()
soni_delhi.sonify()

soni_nyc = SoniSeries(tbl, timecol = 'timestep', val_col = 'new_york_city_temp')
print(numpy.isnan(df.new_york_city_temp).any()) # returns False only if there is a number at every position in that column