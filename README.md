This is a program created to use and edit csv files, and also display data in audio format. It was designed to assist visually impaired people with easily being able to go through and hear their data sets.

In order for the program to be useable, the user must do two things:
  - The user must install all of the imports listed at the top of the program. Assuming you are using visual studio code, you can import any module by going into the terminal and typing pip install module name. If the version you are trying to use does not support a certain module, you may have to install another version of python to use.
  - The user must also download the datasets they wish to use as csv files and put them in the same folder as the program. You can download csv files from either Google Sheets or Microsoft Excel.

Here are the user options and their capabilities:
  - upload file: Asks the user for the name of their file. If the name is valid, the other method options arise. If the name is not valid, then the program will ask again for the file name.
  - long data: Displays the entirety of the data. The screen reader will read the column headers first, then rapid fire all of the data points.
  - short data: Allows for the user to see an amount of rows, picked by them, from the top or the bottom of the datasheet.
  - corr: A method by the pandas import that displays the correlation between two different columns. If the two columns are proportional to one another, then the correlation is closer to 1. If they are not related, then the correlation is closer to 0.
  - info: A method by the pandas import that displays the column headings, amount of rows, and other various information about the data set.
  - slope: After asking for the x-axis and y-axis, this method displays the slope.
  - intercept: After asking for the x-axis and y-axis, this method displays the intercept that would be created when a line was made with these axes.
  - edit: Allows the user to fill in empty or null points with the mean, mode, or median of the data set. This is helpful for the info method, as it won’t work if points are null.
  - table: Displays the data points audibly using the numpy array interface, with the x value as the stereo and the y-value as the pitch. Useful when there are many data points that are identical or similar in value.
  - regular: Utilizes the astronify module to plot the data as sound points. Includes the multiplier method that allows for each point to be expanded so that it lasts longer. The  best option for displaying the data audibly.
  - increment: Utilizes the astronify module to plot the data as sound points. Uses the x value to determine how long each y-value should last, so that x-value is the time and the y-value is the pitch. Useful when regular and table sound off.
  - exit: Allows for the user to exit the program. This option is available for almost any user input method.
