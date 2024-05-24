import pandas as pd
import numpy as np

# current user options: long data, short data, correlation, info, row, exit, slope, and edit

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
        try:
            rows = int(input("Please type how many rows you would like to see: "))
        except:
            print("Not an integer, sending you back to main menu.")
            user_menu(fileName)
        headortail = input("Please type either head or tail: ")
        short_data(fileName, rows, headortail)
    elif (user_choice == "corr"):
        try:
            print(fileName.corr())
        except:
            print("The data is not all integers, so correlations can't be made.")
            print("Returning to main menu.")
    elif (user_choice == "info"):
        print(fileName.info())
    elif (user_choice == "row"):
        user_row = int(input("Which row number would you like to see: "))
        try:
            print("\n" + str(fileName.loc[user_row]))
        except:
            print("Row was invalid, sending back to main menu.")
    elif (user_choice == "exit"):
        exit()
    elif (user_choice == "slope"):
        slope_menu(fileName)
    elif (user_choice == "edit"):
        edit_columns(fileName)
    else:
        print("Not a valid option. Returning you to menu.")
    if (user_choice != "exit"):
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
        print("\n" + str(fileName.head(number_rows)))
    elif (head_or_tail == "tail"):
        print("\n" + str(fileName.tail(number_rows)))
    else:
        print("Not a valid response. Going back to menu.")


def edit_columns(fileName):
    key_list = display_stats(fileName)
    key = input("Which key would you like to edit: ")
    def edit(fileName, column, m_method):
        if (m_method == "mean"):
            fileName.fillna({column: fileName[column].mean()}, inplace = True)
        elif (m_method == "median"):
            fileName.fillna({column: fileName[column].median()}, inplace = True)
        elif (m_method == "mode"):
            fileName.fillna({column: fileName[column].mode()}, inplace = True)
        print("Filed edited. Returning to main menu.")
    if key in key_list:
        whichm = input("Would you like to use mean, median, or mode? ")
        if ((whichm == "mean") or (whichm == "median") or (whichm == "mode")):
            edit(fileName, key, whichm)
        else:
            print("Your selection for mean, median, or mode was invalid.")
    else:
        print("The key you entered was invalid.")


def slope_menu(fileName):
    x_axis = fileName[input("Enter you x_axis: ")]
    y_axis = fileName[input("Enter your y_axis: ")]
    graph_degree = input("Enter the degree of the formula: ")
    try:
        print(f"The slope for your selected axes is {np.polyfit(x_axis, y_axis, graph_degree)}.")
    except:
        print("One of the parameters you typed was incorrect, going back to main menu.")

upload_file()
