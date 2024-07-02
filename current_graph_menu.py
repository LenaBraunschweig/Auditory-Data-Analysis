from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd
import simpleaudio as sa
import numpy as np
import math
from pyo import *

file = input("What is the name of your csv file? ") + ".csv"
file_reader = pd.read_csv(file)

def graph_menu(userFile, userChoice):
  tbl = ''
  if (userChoice == "table"):
    table_xvals(userFile)
  else:
    if (userChoice == "regular"):
      tbl = regular_xvals(userFile)
    else:
      tbl = incremented_xvals(userFile)
    wave_name = input("What would you like your WAV file to be named? ") + ".wav"
    try:
      soni_phys = SoniSeries(data = tbl)
      soni_phys.sonify()
      soni_phys.write(wave_name)
    except:
      print("The file you have choosen didn't work.")
    

def regular_xvals(file):
  x_axis = list(file[input("What is the x_axis: ")])
  y_axis = list(file[input("What is the y_axis: ")])

  def det_multiplier():
    global multiplier
    try:
      multiplier = int(input("What do you want your multiplier to be? "))
    except:
      print("Multiplier not valid, calculating default one.")
      if (len(x_axis) < 1000):
        multiplier = 1000
      elif (len(x_axis) < 10000):
        multiplier = 100
      else:
        multiplier = 10
  
  def fill_missing_points(point1, point2):
    det_multiplier()
    missing_points = []
    difference = point2 - point1
    if (point1 != point2):
      for index in range(1, multiplier + 1):
        new_point = point1 + ((difference/multiplier))
        difference += (point2 - point1)
        missing_points.append(new_point)
    return missing_points

  new_xaxis = []
  new_yaxis = []
  for index in range(len(x_axis) - 1):
    for x_val in fill_missing_points(x_axis[index], x_axis[index + 1]):
      new_xaxis.append(x_val)
    for y_val in fill_missing_points(y_axis[index], y_axis[index + 1]):
      new_yaxis.append(y_val)

  data_table = Table({"time": new_xaxis, "flux": new_yaxis})
  return data_table


def incremented_xvals(file):
  x_axis = list(file[input("What is the x_axis: ")])
  y_axis = list(file[input("What is the y_axis: ")])

  def det_multiplier():
    global multiplier
    global min_val
    copy_x = x_axis.copy()
    min_val = min(x_axis)
    while (math.ceil(min_val) == 0):
      copy_x.remove(min_val)
      min_val = min(copy_x)
    try:
      multiplier = int(input("What do you want your multiplier to be? "))
    except:
      print("Multiplier not valid, calculating default one.")
      multiplier = 1
      while (min_val <= 10):
        multiplier *= 10
        min_val *= 10
    return multiplier

  def multiply():
    det_multiplier()
    multipliers = []
    for x_val in x_axis:
      if (x_val == 0):
        multipliers.append(round((min_val/len(x_axis))*multiplier))
      else:
        multipliers.append(round((multiplier * x_val)))
    return multipliers
  
  def fill_missing_points(multi, point1, point2):
    missing_points = []
    difference = point2 - point1
    if (point1 != point2):
      for index in range(1, multi + 1):
        new_point = point1 + ((difference/multi))
        difference += (point2 - point1)
        missing_points.append(new_point)
    else:
      for index in range(1, multi + 1):
        missing_points.append(point1)
    return missing_points

  new_xaxis = []
  new_yaxis = []
  multis = multiply()

  for index in range(len(x_axis) - 1):
    for x_val in fill_missing_points(multis[index], x_axis[index], x_axis[index + 1]):
      new_xaxis.append(x_val)
    for y_val in fill_missing_points(multis[index], y_axis[index], y_axis[index + 1]):
      new_yaxis.append(y_val)
  
  data_table = Table({"time": new_xaxis, "flux": new_yaxis})
  return data_table

def table_xvals(file):
  x_axis = list(file[input("What is the x_axis: ")])
  y_axis = list(file[input("What is the y_axis: ")])

  def find_freq(y_val):
    offset = 32676
    allowed_freqeuncies = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
    if (y_val <= offset):
      frequency = allowed_freqeuncies[0]
    elif (y_val <= (offset * 10**3)):
      frequency = allowed_freqeuncies[1]
    elif (y_val <= (offset * 10**6)):
      frequency = allowed_freqeuncies[2]
    elif (y_val <= (offset * 10**9)):
      frequency = allowed_freqeuncies[3]
    elif (y_val <= (offset * 10**12)):
      frequency = allowed_freqeuncies[4]
    elif (y_val <= (offset * 10**15)):
      frequency = allowed_freqeuncies[5]
    elif (y_val <= (offset * 10**18)):
      frequency = allowed_freqeuncies[6]
    elif (y_val <= (offset * 10**21)):
      frequency = allowed_freqeuncies[7]
    elif (y_val <= (offset * 10**24)):
      frequency = allowed_freqeuncies[8]
    else:
      frequency = allowed_freqeuncies[9]
    return frequency

  def find_byte_samp(x_val, y_val):
    if (x_val >= 0 and y_val >= 0):
      byte_samp = 2
    elif (x_val < 0 and y_val >= 0):
      byte_samp = 1
    elif (x_val >= 0 and y_val < 0):
      byte_samp = 3
    else:
      byte_samp = 4
    return byte_samp

  def create_lists():
    vals_list = []
    current_xvals = [x_axis[0]]
    current_yvals = [y_axis[0]]

    for index in range(1, len(x_axis)):
      if ((find_freq(y_axis[index]) != find_freq(y_axis[index - 1])) or (find_byte_samp(x_axis[index], y_axis[index]) != find_byte_samp(x_axis[index -1], y_axis[index - 1]))):
        vals_list.append(current_xvals)
        vals_list.append(current_yvals)
        current_xvals = []
        current_yvals = []
      current_xvals.append(x_axis[index])
      current_yvals.append(y_axis[index])
    vals_list.append(current_xvals)
    vals_list.append(current_yvals)
    return vals_list

  def create_numpy(lists):
    def sum(number):
      if number == 0:
        return 0
      elif number == 1:
        return 1
      else:
        return number + sum((number - 1))
    
    numpy_lists = []
    index = 0
    for list in lists:
      previous_index = 0
      current_index = 1
      if (index % 2 == 0):
        current_nump = np.zeros((sum(len(list) - 1), 2))
        column_number = 0
      else:
        column_number = 1
      for internal_index in range(len(list)):
          current_nump[previous_index:current_index, column_number] = math.ceil(list[internal_index])
          previous_index = current_index
          current_index = sum((internal_index + 1))
      if (column_number == 1):
        numpy_lists.append(current_nump)
      index += 1
    return numpy_lists

  def edit_points(pattern_dict):
    for nump in pattern_dict:
      for item in nump:
        item *= round((32767 / max(nump[0])), 0)
    return pattern_dict

  def play_points(nump_list):
    for nump in nump_list:
      play_obj = sa.play_buffer(nump, 2, find_byte_samp(nump[0,0], nump[0,1]), find_freq(nump[0,1]))
      play_obj.wait_done()

  play_points(edit_points(create_numpy(create_lists())))

graph_menu(file_reader, "table")