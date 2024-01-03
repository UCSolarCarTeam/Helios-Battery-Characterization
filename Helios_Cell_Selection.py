
from Albert_Function import voltage_current_table
from argparse import ArgumentParser
import sys
from typing import Union
import pandas as pd

def full_cells():
    """
    Generates a dictionary where keys are CSV file names and values are lists of cell identifiers.

    Returns:
    dict: A dictionary containing CSV file names as keys and lists of cell identifiers as values.
    """
    # Initialize an empty dictionary to store cell information
    cell_csv_dict = {}
    
    # Iterate through cartons from 1 to 18
    for carton in range(1, 19):
        # Iterate through two ends, 'a' and 'b'
        for end in ['a', 'b']:
            # Initialize an empty list to store cell identifiers
            cell_list = []
            
            # Generate the CSV file name based on carton and end
            name = f"Cycle_Test_Carton_{abs(carton):02}{end}.csv"
            
            # Iterate through columns from 1 to 13
            for column in range(1, 14):
                # Depending on the end, iterate through rows and generate cell identifiers
                if end == 'a':
                    for row in range(1, 6):
                        cell = f"{column:02}-{row:02}-{carton:02}"
                        cell_list.append(cell)
                elif end == 'b':
                    for row in range(6, 11):
                        cell = f"{column:02}-{row:02}-{carton:02}"
                        cell_list.append(cell)
            
            # Assign the list of cell identifiers to the corresponding CSV file name in the dictionary
            cell_csv_dict[name] = cell_list
    
    # Return the dictionary containing cell information
    return cell_csv_dict

def cli(args: Union[list[str], None] = None) -> tuple[tuple[str, str], float]:
    """Runs an ArgumentParser on args

    1. An optional argument -p ACCEPTABLE_PERCENTAGE, -percentage ACCEPTABLE_PERCENTAGE: overwrites the acceptable percentage 
    2. An optional argument -c CELL_ID CSV_NAME, --cell_lookup CELL_ID CSV_NAME: print graphs and data from that cell


    args: item to parse, either a list[str] or
                        None in which case sys.argv is parsed

    returns: tuple(resource:bool (required),
                cell_lookup:str (optional, default="")
                )
    """
    
    if args is None:
        args = sys.argv[1:]

   
    parser = ArgumentParser(description = 'cell data')
    parser.add_argument('-c', '--cell_lookup', nargs =2, metavar=('CELL_ID','CSV_NAME'), help = 'get information about the cell selected with CELL_ID and CSV_NAME')
    parser.add_argument('-p', '--percentage', metavar='ACCEPTABLE_PERCENTAGE', help = 'reset the acceptable percentage of the cells')

    arguments = parser.parse_args(args)
    if arguments.cell_lookup == None:
        arguments.cell_lookup = ('FULL','FULL')
    if arguments.percentage == None:
        arguments.percentage = 0.68
    

    return(arguments.cell_lookup, arguments.percentage)

def main():
    # Parse command-line arguments using the 'cli' function
    arguments = cli()
    print(arguments)

    # Check if the first argument is "FULL"
    if arguments[0][0] == "FULL":
        # If it is "FULL", retrieve a dictionary of cell data using the 'full_cells' function
        cell_csv_dict = full_cells()
        percentage = arguments[1]
        
        # Iterate through each CSV file in the dictionary
        for csv in cell_csv_dict:
            # Iterate through each cell in the current CSV file
            for cell in cell_csv_dict[csv]:
                # Open the CSV file in append mode
                with open(csv, 'a') as opened_csv:
                    # Retrieve voltage and current data for the current cell and write it to the CSV
                    cell_data = voltage_current_table(cell, opened_csv)
                    
                    # Calculate the resistance value for the current cell
                    resistance = resistance_value(cell, cell_data, False)
                    
                    # Write the resistance value to the CSV file
                    write_resistance(cell, opened_csv, resistance)
                    
        cell_selection(cell_csv_dict, percentage)

    # If the first argument is not "FULL"
    else:
        # Retrieve the cell and the CSV file name based on the command-line arguments
        cell = arguments[0][0]
        csv = f'Cycle_Test_Carton_{arguments[0][1]}.csv'
        
        # Open the CSV file in append mode
        with open(csv, 'a') as opened_csv:
            # Retrieve voltage and current data for the specified cell and write it to the CSV
            cell_data = voltage_current_table(cell, opened_csv)
            
            # Calculate the resistance value for the specified cell and write it to the CSV
            resistance_value(cell, opened_csv, True)
    


if __name__ == "__main__":
 main()