import matplotlib.pyplot as plt
from keep_Albert_Function import voltage_current_table
import numpy as np
import math as m
import pandas as pd


def resistance_value(cell,voltage_current_list, print_graph):

#
    # Plot the first graph (Voltage vs. Time)
    slope, intercept = np.polyfit(pd.to_numeric(voltage_current_list['Current']), pd.to_numeric(voltage_current_list['Voltage']), 1)

# Create the fitted line using the slope and intercept
    fitted_line = slope * pd.to_numeric(voltage_current_list['Voltage']) + intercept
    if print_graph == 1:
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[1].plot(voltage_current_list['Current'],fitted_line, label=f'Fitted Line: y = {slope:.4f}x + {intercept:.2f}', color='red')
        axs[1].legend()
        axs[1].set_title(f'{cell} Fitted Line')
        axs[1].set_xticks([voltage_current_list['Current'][0],voltage_current_list['Current'][len(voltage_current_list['Voltage'])//4],voltage_current_list['Current'][len(voltage_current_list['Voltage'])//2],voltage_current_list['Current'][3*len(voltage_current_list['Voltage'])//4],voltage_current_list['Current'][len(voltage_current_list['Voltage'])-1]])
        axs[0].plot(voltage_current_list['Current'], voltage_current_list['Voltage'], marker='o', linestyle='-', color='blue', label='Voltage')
        axs[0].set_xlabel('Current')
        axs[0].set_ylabel('Voltage', color='blue')
        axs[0].tick_params(axis='y', labelcolor='blue')
        axs[0].set_title('Current Sweep')
        axs[0].set_yticks([voltage_current_list['Voltage'][0],voltage_current_list['Voltage'][len(voltage_current_list['Voltage'])//4],voltage_current_list['Voltage'][len(voltage_current_list['Voltage'])//2],voltage_current_list['Voltage'][3*len(voltage_current_list['Voltage'])//4],voltage_current_list['Voltage'][len(voltage_current_list['Voltage'])-1]])
        axs[0].set_xticks([voltage_current_list['Current'][0],voltage_current_list['Current'][len(voltage_current_list['Voltage'])//4],voltage_current_list['Current'][len(voltage_current_list['Voltage'])//2],voltage_current_list['Current'][3*len(voltage_current_list['Voltage'])//4],voltage_current_list['Current'][len(voltage_current_list['Voltage'])-1]])
        plt.show()
        
    return(slope)


def main():

    
    cell_data = voltage_current_table('01-02-12', 'Cycle_Test_Carton_12a.csv')
    

    print(resistance_value('01-01-12',cell_data, 1))
    

if __name__ =='__main__':
    main()