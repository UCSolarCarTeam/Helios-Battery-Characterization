import pandas as pd
import math

def is_float(value):
    """Determines if the voltage or current value in the CSV is a float.
    Using try and except to see whether a ValueError would occur during casting.
    Casting is permitted for a blank cell so False is returned when a blank cell is checked.
    
    Argument: value -- string representing a cell in the csv file
    Return value is boolean representing True if the value is a float and False if it is not a float

    """
    try: # Checks if casting will occur
        if math.isnan(float(value)): # Checks if the cell is a blank cell
            return False # Returns False if NaN results from casting
        else: 
            return True # Returns True if casting is possible
    except ValueError: # If ValueError occurs it will return False
        return False

def voltage_current_table(cell_number, csv_file):
    """Processes the data from the inputted csv file and outputs a dataframe containing Voltage and Current values for the battery during the test.
    Processing occurs by parsing through data to see where both the Voltage and Current Values are floats for the particular cell number and appends them into a Pandas dataframe.
    
    
    Arguments:
    cell_number -- string representing the cell number within the csv file
    csv_file -- csv file representing the original data collected from battery testing

    Return value: processed_data -- A 2-columned Pandas dataframe representing the voltage and current values for the battery during the test

    """ 
    voltage_list = [] # Empty voltage list initialized
    current_list = [] # Empty current list initialized

    with open(csv_file, 'a+') as opened_csv: # Opens csv file to append, read, and write
        opened_csv.seek(0) # Sets the file pointer position to the start of the csv
        original_data = pd.read_csv(opened_csv) # Reads CSV file into a Pandas dataframe
        max_index = len(original_data['Date & Time']) - 1 # Gives max index in csv file (specifically in the 'Date & Time' column)
        cell_index = original_data.index[original_data['Cell Number'] == cell_number][0] # Finds index number at given cell number

        voltage_col_num = original_data.columns.get_loc('Voltage') # Gets column number of voltage header
        current_col_num = original_data.columns.get_loc('Current') # Gets column number of current header

        for index in range(cell_index, max_index): # For loop created to iterate through rows of CSV
            volt_value = original_data.iloc[index, voltage_col_num] # Voltage value at specific row
            curr_value = original_data.iloc[index, current_col_num] # Current value at specific row

            if is_float(volt_value) and is_float(curr_value): # Checks to see if voltage value and current value is a float
                voltage_list.append(volt_value) # Adds voltage value to the list
                current_list.append(curr_value) # Adds current value to the list

            elif volt_value == 'Voltage': # Checks to see if the voltage and current values of the full cell is iterated through
                break # Breaks loop once full cell is iterated through
        
        voltage_title = 'Voltage' # Creates name for new voltage column
        current_title = 'Current' # Creates name for new current column
        data = {voltage_title: voltage_list, current_title: current_list} # Dictionary containing data and columns
        processed_data = pd.DataFrame(data) # Dataframe created containing dictionary
        empty_index_list = [''] * len(processed_data) # Creates new list of empty strings to 'hide' index column when outputting dataframe
        processed_data.index = empty_index_list # Applies the new list of empty strings onto the dataframe

        return processed_data # Returns the dataframe containing voltages and currents to the function
    
'''the dataframes should have clearer names
    please write proper function definitions, in 233 I'm pretty sure you've used them before
    have you tested this code?
    do you know how try and except work?'''