import pandas as pd
import numpy as np

# current user options: long data, short data, correlation, info, row, exit, slope, and edit

def upload_file():
    file = ""
    file = input("\nPlease enter the name of the CSV file: ") + ".csv"
    if file == "exit.csv":
        quit()
    try:
        fileFrame = pd.read_csv(file)
        display_stats(fileFrame)
        user_menu(fileFrame)
    except:
        print("File is not valid, please try again with a different file name.")
        upload_file()

def user_menu(fileName):
    user_choice = input("\nPlease type out what you would like to do with this data: ")
    if (user_choice == "long data"):
        print(fileName.to_string())
    # need to fix this method
    elif (user_choice == "short data"):
        rows = input("Please type how many rows you would like to see: ")
        headortail = input("Please type either head or tail: ")
        short_data(fileName, rows, headortail)
    elif (user_choice == "correlation"):
        print(fileName.corr())
    elif (user_choice == "info"):
        print(fileName.info())
    elif (user_choice == "row"):
        user_row = input("Which row number would you like to see: ")
        try:
            print(fileName.loc(user_row))
        except:
            print("Row was invalid, sending back to main menu.")
            user_menu(fileName)
    elif (user_choice == "exit"):
        quit()
    elif (user_choice == "slope"):
        slope_menu(fileName)
    elif (user_choice == "edit"):
        fileName = edit_columns()
    else:
        print("Not a valid option. Returning you to menu.")
    user_menu(fileName)


def display_stats(fileName):
    global keys
    keys = []
    for key in fileName.keys():
        keys.append(key)
    print("\nThe keys for this data set are:")
    for key in keys:
        print(key)
    rows = len(fileName)
    print(f"\nThere are {rows} rows in this data spread")
    return keys

def short_data(fileName, number_rows, head_or_tail):
    if (head_or_tail == "head"):
        print(fileName.head(number_rows))
    elif (head_or_tail == "tail"):
        print(fileName.tail(number_rows))
    else:
        print("Not a valid response. Going back to menu.")


def edit_columns(fileName):
    new_file = fileName
    key = input("Which key would you like to edit: ")
    key_list = display_stats(fileName)
    if key in key_list:
        whichm = input("Would you like to use mean, median, or mode? ")
        try:
            new_file = edit(fileName, key, whichm)
        except:
            print("Your selection for mean, median, or mode was invalid.")
    else:
        print("The key you entered was invalid.")
    return new_file

def slope_menu(fileName):
    x_axis = fileName[input("Enter you x_axis: ")]
    y_axis = fileName[input("Enter your y_axis: ")]
    #graph_type = input("Enter the type of graph: ")
    try:
        # need to edit this to include the graph type
        # the default of the 1 is a linear graph
        print(f"The slope for your selected axes is {np.polyfit(x_axis, y_axis, 1)}.")
    except:
        print("One of the parameters you typed was incorrect, going back to main menu.")


def edit(fileName, column, m_method):
    fileName.fillna({column: fileName[column].m_method()}, inplace = True)
    return fileName

upload_file()
