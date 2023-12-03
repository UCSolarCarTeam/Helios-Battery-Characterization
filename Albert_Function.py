def voltage_current1(cell_number, csv_file): 
    # Following function is for specific CSV for one battery or if there are multiple CSVs containing multiple batteries
    with open(csv_file, 'r'): # opens and reads csv file
        df1 = pd.read_csv(csv_file) # reads CSV file
        voltage_list = df1['Voltage'].tolist() # Turns voltage column to list
        current_list = df1['Current'].tolist() # Turns current column to list
        voltage_title = f'Voltage for {cell_number}' # Creates name for new voltage column
        current_title = f'Current for {cell_number}' # Creates name for new current column
        data = {voltage_title: voltage_list, current_title: current_list} # Dictionary containing data and columns
        df3 = pd.DataFrame(data) # Dataframe created containing dictionary
        return df3 

def voltage_current2(cell_number, csv_file): #Following block of code is for one huge CSV containing mulitple batteries
        with open(csv_file, 'r'): # opens and reads csv file
            df1 = pd.read_csv(csv_file) # reads CSV file
            cell_specs = df1[cell_number] # Reads the Cell number column
            voltage_list = cell_specs['Voltage'].tolist() # Assuming that voltage and current columns are within the cell_num columns
            current_list = cell_specs['Current'].tolist()
            data = {'Voltage': voltage_list, 'Current': current_list} # Dictionary containing data and columns
            df3 = pd.DataFrame(data) # Dataframe created containing dictionary
            return df3