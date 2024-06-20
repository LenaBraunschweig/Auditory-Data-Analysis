import pandas as pd
import numpy as np

# current user options: long data, short data, correlation, info, row, edit, slope, intercept, and exit

def upload_file():
    file = ""
    file = input("\nPlease enter the name of the CSV file: ") + ".csv"
    if file == "exit.csv":
        exit()
    try:
        fileFrame = pd.read_csv(file, index_col = 0)
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
    try:
            rows = int(input("Please type how many rows you would like to see: "))
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
    user_row = int(input("Which row number would you like to see: "))
    try:
        print("\n" + str(userFile.loc[user_row]))
    except:
        print("Row was invalid, sending back to main menu.")


def edit_columns(userFile):
    key_list = display_stats(userFile)
    key = input("Which key would you like to edit: ")
    def edit(userFile, column, m_method):
        if (m_method == "mean"):
            userFile.fillna({column: userFile[column].mean()}, inplace = True)
        elif (m_method == "median"):
            userFile.fillna({column: userFile[column].median()}, inplace = True)
        elif (m_method == "mode"):
            userFile.fillna({column: userFile[column].mode()}, inplace = True)
        print("Filed edited. Returning to main menu.")
    if key in key_list:
        whichm = input("Would you like to use mean, median, or mode? ")
        if ((whichm == "mean") or (whichm == "median") or (whichm == "mode")):
            edit(userFile, key, whichm)
        else:
            print("Your selection for mean, median, or mode was invalid.")
    else:
        print("The key you entered was invalid.")


def slope_menu(userFile, choice):
    x_axis = input("Enter your x_axis: ")
    y_axis = input("Enter your y_axis: ")
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

upload_file()