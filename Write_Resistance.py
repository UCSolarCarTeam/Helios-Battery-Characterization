import pandas as pd
import math

'''
    records the resistance of a battery cell from given data

    Inputs:
    Cell number (str)
    CSV as a filename opened as append
    Resistance value (float)

    Output:
    The resistance value of given cell as a new column in CSV called resistance
'''


def write_resistance(cell_number, csv_filename, resistance_value):
    '''
    records the resistance of a battery cell from given data

    Inputs:
    Cell number (str)
    CSV as a filename opened as append
    Resistance value (float)

    Output:
    resistance value of given cell as a new column in CSV called resistance
    '''
    cell_data = pd.read_csv(csv_filename)

    if "Resistance" not in cell_data.columns:
        
        cell_data.insert(len(cell_data.columns), "Resistance", "", True)


    cell_row = cell_data['Cell Number'] == cell_number

    cell_data.loc[cell_row, "Resistance"] = resistance_value


def main():
    write_resistance('01-01-01','Helios-Battery-Characterization-master\Cycle_Test_Carton_01a.csv',1) # Hardcoded for testing


if __name__ == '__main__':
    main()