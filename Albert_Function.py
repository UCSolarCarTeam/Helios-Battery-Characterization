import pandas as pd

def is_float(value): # Function to check if the voltage or current value in the CSV is a float
    try: # Checks if casting will occur
        float(value) 
        return True # Returns True if casting is possible
    except ValueError: # If ValueError occurs it will return False
        return False

def voltage_current(cell_number, csv_file): 
    voltage_list = [] # Empty voltage list initialized
    current_list = [] # Empty current list initialized

    with open(csv_file, 'a'): # Opens and reads csv file
        df1 = pd.read_csv(csv_file) # Reads CSV file
        max_index = df1['Date & Time'].idxmax() # Gives max index in csv file (specifically in the 'Date & Time' column)
        cell_index = df1.index[df1['Cell Number'] == cell_number][0] # Finds index number at given cell number

        voltage_col_num = df1.columns.get_loc('Voltage') # Gets column number of voltage header
        current_col_num = df1.columns.get_loc('Current') # Gets column number of current header

        for index in range(cell_index, max_index): # For loop created to iterate through rows of CSV
            volt_value = df1.iloc[index, voltage_col_num] # Voltage value at specific row
            curr_value = df1.iloc[index, current_col_num] # Current value at specific row

            if is_float(volt_value) and is_float(curr_value): # checks to see if voltage value and current value is a float
                voltage_list.append(volt_value) # Adds voltage value to the list
                current_list.append(curr_value) # Adds current value to the list

            elif volt_value == 'Voltage': # Checks to see if the voltage and current values of the full cell is iterated through
                break # Breaks loop once full cell is iterated through
        
        voltage_title = f'Voltage for {cell_number}' # Creates name for new voltage column
        current_title = f'Current for {cell_number}' # Creates name for new current column
        data = {voltage_title: voltage_list, current_title: current_list} # Dictionary containing data and columns
        df2 = pd.DataFrame(data) # Dataframe created containing dictionary
        return df2 # Returns the dataframe containing voltages and currents to the function