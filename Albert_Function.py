import pandas as pd
import math


def main(): # Main function of script
    """Outputs the dataframe of all voltage and current values for a specific cell during the battery cell characterization tests.

    No arguments
    No return value but outputs the processed data as a dataframe.

    """
    with open('Cycle_Test_Carton_01a.csv', 'a+') as opened_csv: # Opens test csv file to append, read, and write
        print(voltage_current_table('01-01-01', opened_csv)) # Outputs the processed data for the specfic cell from a CSV


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

def voltage_current_table(cell_number:str, opened_csv:str):
    """Processes the data from the inputted csv file and outputs a dataframe containing Voltage and Current values for the battery during the test.
    Processing occurs by parsing through data to see where both the Voltage and Current Values are floats for the particular cell number and appends them into a Pandas dataframe.
    
    
    Arguments:
    cell_number -- string representing the cell number within the csv file
    csv_file -- csv file representing the original data collected from battery testing

    Return value: processed_data -- A 2-columned Pandas dataframe representing the voltage and current values for the battery during the test

    """ 
    voltage_list = [] # Empty voltage list initialized
    current_list = [] # Empty current list initialized
    opened_csv.seek(0) # Sets the file pointer position to the start of the csv
    original_data = pd.read_csv(opened_csv) # Reads CSV file into a Pandas dataframe

    try:
        max_index = len(original_data['Date & Time']) - 1 # Gives max index in csv file (specifically in the 'Date & Time' column)
    
    except KeyError: # Raises an exception to a NameError
        print('This csv is empty or incorrectly formatted for this code.') # Alerts user that CSV is empty of incorrectly formatted
        quit() # Ends the program
        

    if '-' in cell_number: # Checks for hyphen in code to see if cell number is formatted correctly
        try: # A try and except statement to determine if the cell number is within CSV
            cell_index = original_data.index[original_data['Cell Number'] == cell_number][0] # Finds index number at given cell number

        except IndexError: # Raises an exception to an IndexError
            print("This cell is not within the inputted CSV file. Ensure that cell number is inputted in correct format: column-row-carton") # Outputs error message
            quit() # Ends the program 
    
    else:
        print('Cell Number not in correct format. The following is the correct format: column-row-carton') # Alerts user that cell number is in incorrect format
        quit() # Ends the program

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

    return processed_data # Returns the dataframe containing voltages and currents to the function "can also do

if __name__ == "__main__": # Runs the main function if this is the file being run
    main() # Calls the main function
