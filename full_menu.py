from astropy.table import Table
from astronify.series import SoniSeries
import pandas as pd
import simpleaudio as sa
import numpy as np
import math
from pyo import *

# current user options: long data, short data, correlation, info, row, edit, slope, intercept, table, regular, increment, and exit

def upload_file():
  file = ""
  file = input("\nPlease enter the name of the CSV file: ") + ".csv"
  if file == "exit.csv":
    exit()
  try:
    fileFrame = pd.read_csv(file)
  except:
    print("File is not valid, please try again with a different file name.")
    upload_file()
  display_stats(fileFrame)
  user_menu(fileFrame)

def user_menu(fileName):
  user_choice = input("\nPlease type out what you would like to do with this data: ")
  if (user_choice == "long data"):
    print(fileName.to_string())
  elif (user_choice == "short data"):
    short_data_menu(fileName)
  elif (user_choice == "corr"):
    corr_menu(fileName)
  elif (user_choice == "info"):
    print(fileName.info())
  elif (user_choice == "row"):
    row_menu(fileName)
  elif (user_choice == "exit"):
    exit()
  elif (user_choice == "slope" or user_choice == "intercept"):
    slope_menu(fileName, user_choice)
  elif (user_choice == "edit"):
    edit_columns(fileName)
  elif ((user_choice == "table") or (user_choice == "regular") or (user_choice == "increment")):
    graph_menu(fileName, user_choice)
  else:
    print("Not a valid option. Returning you to menu.")
  
  if (user_choice != "exit"):
    user_menu(fileName)


def display_stats(userFile):
  global keys
  keys = []
  for key in userFile.keys():
    keys.append(key)
  print("\nThe keys for this data set are:")
  for key in keys:
    print(key)
  rows = len(userFile)
  print(f"\nThere are {rows} rows in this data spread")
  return keys


def short_data_menu(userFile):
  def short_data(userFile, number_rows, head_or_tail):
    if (head_or_tail == "head"):
      print("\n" + str(userFile.head(number_rows)))
    elif (head_or_tail == "tail"):
      print("\n" + str(userFile.tail(number_rows)))
    else:
      print("Not a valid response. Going back to menu.")
  rows = input("Please type how many rows you would like to see: ")
  if (rows == "exit"):
    exit()
  else:
    try:
      rows = int(rows)
    except:
      print("Not an integer, sending you back to main menu.")
      user_menu(userFile)
    headortail = input("Please type either head or tail: ")
    short_data(userFile, rows, headortail)


def corr_menu(userFile):
  try:
    print(userFile.corr())
  except:
    print("The data is not all integers, so correlations can't be made.")
    print("Returning to main menu.")


def row_menu(userFile):
  user_row = input("Which row number would you like to see: ")
  if (user_row == "exit"):
    exit()
  try:
    user_row = int(user_row)
    print("\n" + str(userFile.loc[user_row]))
  except:
    print("Row was invalid, sending back to main menu.")


def edit_columns(userFile):
  key = input("Which key would you like to edit: ")
  def edit(userFile, column, m_method):
    if (m_method == "mean"):
      userFile.fillna({column: userFile[column].mean()}, inplace = True)
    elif (m_method == "median"):
      userFile.fillna({column: userFile[column].median()}, inplace = True)
    elif (m_method == "mode"):
      userFile.fillna({column: userFile[column].mode()}, inplace = True)
    print("Filed edited. Returning to main menu.")
  if key in keys:
    whichm = input("Would you like to use mean, median, or mode? ")
    if ((whichm == "mean") or (whichm == "median") or (whichm == "mode")):
      edit(userFile, key, whichm)
    else:
      print("Your selection for mean, median, or mode was invalid.")
  else:
    print("The key you entered was invalid.")


def slope_menu(userFile, choice):
  x_axis, y_axis = get_axes(userFile)

  if x_axis in keys and y_axis in keys:
    try:
      graph_degree = int(input("Enter the degree of the formula: "))
      if choice == "slope":
        print(f"The slope for your selected axes is {np.polyfit(userFile[x_axis], userFile[y_axis], graph_degree)[0]}.")
      else:
        print(f"The intercept for your selected axes is {np.polyfit(userFile[x_axis], userFile[y_axis], graph_degree)[1]}.")
    except:
      print("One of the parameters you typed was incorrect, going back to main menu.")
  else:
    print("One of the parameters you typed was incorrect, going back to main menu.")

def graph_menu(userFile, userChoice):
  tbl = ''
  if (userChoice == "table"):
    try:
      table_xvals(userFile)
    except:
      print("Returning to main menu.")
  else:
    if (userChoice == "regular"):
      tbl = regular_xvals(userFile)
    else:
      tbl = incremented_xvals(userFile)
    soni_phys = SoniSeries(data = tbl)
    wave_name = input("What would you like your WAV file to be named? ") + ".wav"
    if (wave_name == "exit.wav"):
      exit()
    else:
      try:
        soni_phys.sonify()
        soni_phys.write(wave_name)
      except:
        print("Returning to main menu.")

def get_axes(file):
  x_name = input("What is the x_axis: ")
  y_name = input("What is the y_axis: ")
  if ((x_name == "exit") or (y_name == "exit")):
    exit()
  else: 
    try:
      file = file.sort_values(by = [str(x_name), str(y_name)])
      x_axis = list(file[str(x_name)])
      y_axis = list(file[str(y_name)])
      return x_axis, y_axis
    except:
      print("The axis you have tried to use is invalid.")
      return get_axes(file)

def ask_multiplier():
  global multiplier
  multiplier = input("What do you want your multiplier to be? ")
  try:
    multiplier = int(multiplier)
    while ((multiplier < 1) or (multiplier > 1000)):
      print("Multiplier must be between 10 and 1000.")
      multiplier = int(input("What do you want your new multiplier to be? "))
    return multiplier
  except:
    if (multiplier == "exit"):
      exit()
    else:
      print("Multiplier must be an integer, please try again.")
      return ask_multiplier()

def det_min(xaxis):
  global min_val
  copy_x = xaxis.copy()
  min_val = min(copy_x)
  while (math.ceil(min_val) == 0):
    copy_x.remove(min_val)
    min_val = min(copy_x)
  return min_val

def fill_missing_points(multi, point1, point2):
    try:
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
    except:
      print("The data points must be integers.")

def create_table(xaxis, yaxis):
  data_table = Table({"time": xaxis, "flux": yaxis})
  return data_table

def multiply(xaxis):
  ask_multiplier()
  det_min(xaxis)
  multipliers = []
  for x_val in xaxis:
    if (x_val == 0):
      point = round((min_val/len(xaxis))* multiplier)
    else:
      point = round((multiplier * x_val))
    point += 1
    multipliers.append(point)
  return multipliers

def find_freq(yval):
  offset = 32676
  allowed_freqeuncies = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
  if (yval <= offset):
    frequency = allowed_freqeuncies[0]
  elif (yval <= (offset * 10**3)):
    frequency = allowed_freqeuncies[1]
  elif (yval <= (offset * 10**6)):
    frequency = allowed_freqeuncies[2]
  elif (yval <= (offset * 10**9)):
    frequency = allowed_freqeuncies[3]
  elif (yval <= (offset * 10**12)):
    frequency = allowed_freqeuncies[4]
  elif (yval <= (offset * 10**15)):
    frequency = allowed_freqeuncies[5]
  elif (yval <= (offset * 10**18)):
    frequency = allowed_freqeuncies[6]
  elif (yval <= (offset * 10**21)):
    frequency = allowed_freqeuncies[7]
  elif (yval <= (offset * 10**24)):
    frequency = allowed_freqeuncies[8]
  else:
    frequency = allowed_freqeuncies[9]
  return frequency

def find_byte_samp(xval, yval):
  if (xval >= 0 and yval >= 0):
    byte_samp = 2
  elif (xval < 0 and yval >= 0):
    byte_samp = 1
  elif (xval >= 0 and yval < 0):
    byte_samp = 3
  else:
    byte_samp = 4
  return byte_samp

def create_numpy(lists):
  def sum(number):
    if number == 0:
      return 0
    elif number == 1:
      return 1
    else:
      return number + sum(number - 1)
    
  numpy_lists = []
  index = 0
  space = 0
  for list in lists:
    space = 0
    if (index % 2 == 0):
      current_nump = np.zeros((multiplier * (len(list) - 1), 2))
      column_number = 0
    else:
      column_number = 1
    for internal_index in range(len(list)):
        current_nump[(multiplier * space):(multiplier * (space + 1)), column_number] = math.ceil(list[internal_index])
        space += 1
    if (column_number == 1):
      numpy_lists.append(current_nump)
    index += 1
  return numpy_lists

def create_lists(xaxis, yaxis):
    vals_list = []
    current_xvals = [xaxis[0]]
    current_yvals = [yaxis[0]]
    multis = multiply(xaxis)

    for index in range(1, len(xaxis) - 1):
      if ((find_freq(yaxis[index]) != find_freq(yaxis[index - 1])) or (find_byte_samp(xaxis[index], yaxis[index]) != find_byte_samp(xaxis[index -1], yaxis[index - 1]))):
        vals_list.append(current_xvals)
        vals_list.append(current_yvals)
        current_xvals = []
        current_yvals = []
      for x_val in fill_missing_points(multis[index], xaxis[index], xaxis[index + 1]):
        current_xvals.append(x_val)
      for y_val in fill_missing_points(multis[index], yaxis[index], yaxis[index + 1]):
        current_yvals.append(y_val)
    vals_list.append(current_xvals)
    vals_list.append(current_yvals)
    return vals_list

def regular_xvals(fileName):
  x_axis, y_axis = get_axes(fileName)
  ask_multiplier()
  
  new_xaxis = []
  new_yaxis = []
  
  for index in range(len(x_axis) - 1):
    for x_val in fill_missing_points(multiplier, x_axis[index], x_axis[index + 1]):
      new_xaxis.append(x_val)
    for y_val in fill_missing_points(multiplier, y_axis[index], y_axis[index + 1]):
      new_yaxis.append(y_val)
  
  return create_table(new_xaxis, new_yaxis)

def incremented_xvals(fileName):
  x_axis, y_axis = get_axes(fileName)

  new_xaxis = []
  new_yaxis = []
  multis = multiply(x_axis)

  for index in range(len(x_axis) - 1):
    for x_val in fill_missing_points(multis[index], x_axis[index], x_axis[index + 1]):
      new_xaxis.append(x_val)
    for y_val in fill_missing_points(multis[index], y_axis[index], y_axis[index + 1]):
      new_yaxis.append(y_val)
  
  return create_table(new_xaxis, new_yaxis)

def table_xvals(fileName):
  x_axis, y_axis = get_axes(fileName)

  def edit_points(pattern_dict):
    for nump in pattern_dict:
      for item in nump:
        item *= round((32767 / max(nump[:, 0])), 0)
    return pattern_dict

  def play_points(nump_list):
    for nump in nump_list:
      play_obj = sa.play_buffer(nump, 2, find_byte_samp(nump[0,0], nump[0,1]), find_freq(nump[0,1]))
      play_obj.wait_done()
  
  play_points(edit_points(create_numpy(create_lists(x_axis, y_axis))))

upload_file()