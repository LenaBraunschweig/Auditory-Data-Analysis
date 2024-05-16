import pandas as pd
from Edited_physics_data_practice import editedPhysFrame

def upload_file():
    file = input("Please enter the name of the CSV file:")
    try:
        fileFrame = pd.read_csv(file)
        display_keys(fileFrame)
        user_enter = input("Please type out what you would like to do with this data:")
        user_menu(user_enter)
    except:
        print("File is not valid, please try again with a different file name.")
        upload_file()

def user_menu(user_choice, fileName):
    if (user_choice == "long data"):
        print(fileName.to_string())
    elif (user_choice == "short data"):
        rows = input("Please type how many rows you would like to see:")
        pd.options.display.max_rows = rows
        print(fileName)
    elif (user_choice == "correlation"):
        print(fileName.corr())

def display_keys(fileName):
    keys = []
    for key in fileName.keys():
        keys.append(key)
    print("\nThe keys for this data set are:")
    for key in keys:
        print(key)

