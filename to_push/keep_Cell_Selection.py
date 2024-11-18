'''Function 4:
cell_selection(cell_csv_dict, percentage)
Input:
A dictionary with a list of all cell names in a csv as a value to a key that is the csv name
The acceptable percentage
Output:
A histogram of the resistance values of the cells
A list of the cells that are in the top 16% (dict(csv:list(cells)))
A list of cells that are in the bottom 16%
A list of cells in the middle 68%
Percentage adjustable?
'''
from keep_Helios_Cell_Selection_Jenny import full_cells
from keep_Resistance_Value import resistance_value
import pandas as pd
from keep_Albert_Function import voltage_current_table
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def cell_selection(cell_csv_dict, per):

    resistance_list = []
    cell_list = []
    passed_cells = {}
    #cell_csv_dict = {'Cycle_Test_Carton_12a.csv':['01-01-12']}
    for csv in cell_csv_dict:
        print(csv)
        for cell in cell_csv_dict[csv]:
            cell_data = voltage_current_table(cell, csv)
            resistance = resistance_value(cell, cell_data, 0)
            resistance_list.append(resistance)
            cell_list.append(cell)
   
    data = {'Cell':cell_list,'Resistance':resistance_list}
    resistance_cell_df = pd.DataFrame(data)
    print(len(resistance_cell_df["Resistance"]))

    plt.figure(figsize=(8, 6))
    sns.histplot(resistance_cell_df["Resistance"], kde=True, bins=5, color='skyblue')  # Adjust bins as needed

    # Generating standard Gaussian distribution
    mu, sigma = np.mean(resistance_cell_df["Resistance"]), np.std(resistance_cell_df["Resistance"])
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    gaussian_dist = norm.pdf(x, mu, sigma)

    # Plotting standard Gaussian distribution
    plt.plot(x, gaussian_dist, 'r-', linewidth=2)

    plt.title('Histogram with Standard Gaussian Distribution')
    plt.xlabel('Resistor Value')
    plt.ylabel('Density')
    plt.legend(['Gaussian Distribution', 'Histogram'])
    plt.grid(True)
    plt.show()

    lower_bound = mu - per*sigma
    upper_bound = mu + per*sigma

    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)
    print('std', sigma)
    print('mean', mu)
    
    for cell in range(len(resistance_cell_df['Resistance'])):
        if (resistance_cell_df['Resistance'][cell] > lower_bound):
            if (resistance_cell_df['Resistance'][cell] < upper_bound):
                passed_cells[resistance_cell_df['Cell'][cell]]=resistance_cell_df['Resistance'][cell]
    '''
    for cell in range(len(resistance_cell_df['Resistance'])):
        if (resistance_cell_df['Resistance'][cell] < lower_bound):
           passed_cells[resistance_cell_df['Cell'][cell]]=resistance_cell_df['Resistance'][cell]
        if (resistance_cell_df['Resistance'][cell] > upper_bound):
            passed_cells[resistance_cell_df['Cell'][cell]]=resistance_cell_df['Resistance'][cell]
'''
    for cell in passed_cells:
        print(cell)
    print(len(passed_cells))
    print('std', sigma)
    print('mean', mu)
def main():
    cell_selection(full_cells(),1) # Hardcoded for testing


if __name__ == '__main__':
    main()   
