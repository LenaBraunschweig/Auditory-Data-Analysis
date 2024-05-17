import pandas as pd

def upload_file():
    file = ""
    file = input("\nPlease enter the name of the CSV file: ")
    if file == "exit":
        exit()
    try:
        fileFrame = pd.read_csv(file)
        display_keys(fileFrame)
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
        pd.options.display.max_rows = rows
        print(fileName)
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
            user_menu(user_choice, fileName)
    elif (user_choice == "exit"):
        quit()
    elif (user_choice == "slope"):
        # need to add the slope method
        pass
    elif (user_choice == "edit"):
        edit_rows()
    else:
        print("Not a valid option. Returning you to menu.")
    user_menu(fileName)


def display_keys(fileName):
    global keys
    keys = []
    for key in fileName.keys():
        keys.append(key)
    print("\nThe keys for this data set are:")
    for key in keys:
        print(key)
    # need to display how many rows there are

def edit_rows():
    # need to create an edit rows sub-menu
    pass


upload_file()
