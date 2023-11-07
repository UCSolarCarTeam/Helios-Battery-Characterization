import sys
from time import time, sleep
from datetime import datetime
from PPH_1503D import PPH_1503D
import math as m 
import csv
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk

def take_measurement(stdout_suppressed=False):
    #takes a voltage measurement from the DVM and a current channel 1
    #stdout_supressed is related to weither or not the measurments are printed
    volt_samp = PSU.measure_voltage(1)
    curr_samp = PSU.measure_current(1)

    # Print measurement
    if not stdout_suppressed:
        sys.stdout.write(f'\rBattery Voltage: {volt_samp} V, Battery Current: {curr_samp} A')
        sys.stdout.flush()
    #returns a dictionary with the two measurements
    return {"Batt_Volt": volt_samp,
            "Batt_Curr": curr_samp
            }

def write_measurement(file_handler, measurement):
    #writes the measuremnt disctionary to a file with a time stamp
    file_handler.writerow([datetime.now().strftime("%d-%m-%Y %H:%M:%S"), measurement["Batt_Volt"], measurement["Batt_Curr"]])
    sys.stdout.write('    *Logged')


def take_soc(stdout_suppressed=False):
    #takes a measurements of just the voltgae using the DVM
    #stdout_supressed is related to weither or not the measurments are printed
    volt_samp = PSU.measure_voltage(1)
    

    # Print measurement
    if not stdout_suppressed:
        sys.stdout.write(f'\rBattery Voltage: {volt_samp} V')
        sys.stdout.flush()

    #returns the voltage measurment as a standard measurement dictionary
    return {"Batt_Volt": volt_samp,
           "Batt_Curr": "failed" }

def current_sweep(current_c,size, file_handler ):
    #measure the voltage response of the DUT when a linearly increasing current is applied

    #creates the current points for the sweep
    current =list(abs(np.linspace(0.1*current_c, 0.2*current_c, size)))

    #how fast the SMU changes current
    currentsweep_update_int = 0.5
    #how fast the measurment is written to the data file
    #currentsweep_measure_int = 1

    t_ref_update = time()

    
    #loops through the data points for the current sweep 
    for data in current:
            PSU.set_source_ilim(1, data)
            t_ref_int_update = time()

            measurement = take_measurement()
            write_measurement(file_handler=WRITER, measurement=measurement)

            while (t_ref_int_update - t_ref_update) < currentsweep_update_int:  # timing for updates
            
                t_ref_int_update = time()
            
            t_ref_update = t_ref_int_update



def ac_impedance(current_c, size, file_handler):
    #measures the voltage responce of the DUT when a sinusiodal current is applied to it

    #created the currents points for the sinusoid
    ac_impedance_current = [0.5*(m.cos(point*2*m.pi)) for point in np.linspace(0,1,size)]

    ac_impedance_current = [point + 1 for point in ac_impedance_current]    

    #update period for the current to change 1hz * 50 steps = 50 khz 
    ac_impedance_update_int = 0.00002
    #update period for the measurments to be written
    t_ref_update = time()


    #loops the sinusoid 2 times
    for loop in range(0,2):
        for data in ac_impedance_current:
                PSU.set_source_ilim(1, data)
                t_ref_int_update = time()

                measurement = take_measurement()
                write_measurement(file_handler=WRITER, measurement=measurement)

                while (t_ref_int_update - t_ref_update) < ac_impedance_update_int:  # timing for updates
                
                    t_ref_int_update = time()
                
                t_ref_update = t_ref_int_update
    

    '''for i in range(0,6,1):
        #loops through the data
        for data in ac_impedance_current:
            t_ref_int_update = time()
            t_ref_int_measurement = time()

            if (t_ref_int_update - t_ref_update) >= ac_impedance_update_int:  # timing for updates
                t_ref_update = t_ref_int_update
                PSU.set_source_ilim(1, data)
                measurement = take_measurement()

            if (t_ref_int_measurement - t_ref_measurement) >= ac_impedance_measure_int:  # timing for measurements
                t_ref_measurement = t_ref_int_measurement
                measurement=take_measurement()
                write_measurement(file_handler=WRITER, measurement=measurement)'''
     
    

def exit_all():
    print('PSU output disabled - exiting.')
    PSU.output_state(1, 'OFF')
    PSU.__del__()
    exit()
#

class CellSelectionFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()

        self.cellvar = tk.StringVar()

        self.make_widgets()

        self.country.focus_set()

    def make_widgets(self):
        self.country = ttk.Entry(self, textvariable=self.cellvar)
        self.country.grid()

        self.country.bind("<Return>", lambda event = None: self.start_test())

        ttk.Button(self, text="Start Test", command=self.start_test).grid()

    def start_test(self):
        self.cell_value = self.cellvar.get()  # Store the value in an instance variable
        self.master.quit()  # This will exit the GUI

    def get_cell_value(self):
        return self.cell_value

if __name__ == "__main__":
    # Setup
    PSU = PPH_1503D('USB0::0x2184::0x002C::GEQ837356::3::INSTR') #USB0::0x2184::0x002C::GEQ837356::3::INSTR
    PSU.set_outp_ovp(1, 4.6)
    PSU.set_outp_ovp_state(1, 'ON')
    PSU.set_data_format('SREal')
    PSU.set_sense_func(1, 'VOl')
    PSU.set_sense_period(1, 1)
    PSU.set_sense_averaging(1, 10)

        # Test parameters
       # Interval between log writes in seconds


    root = tk.Tk()
    input = CellSelectionFrame(root)
    root.mainloop()

    CHARGE_V = 4.4
    C = 4.8                      # 1 C
    CHARGE_TERM_I = 0.03         # 0.02 Cmin
    DISCHARGE_I = -0.075         # 0.04 Cmin
    DISCHARGE_TERM_V = 3.0
    SIZE = 50                     #size of the measurements



    cell_value = input.get_cell_value()
    parts = cell_value.split('-')  
    carton = parts[-1]  

    # Log setup 
    FILENAME = f'Cycle Test Carton {carton}.csv'
    with open(FILENAME, 'a', newline='') as F:
        try:
            #run tests
            WRITER = csv.writer(F)  
            WRITER.writerow(["Date & Time", 'Voltage', 'Current', "Cell Number"])
            WRITER.writerow(['','','',cell_value])

            PSU.set_source_voltage(1, 3.8)#set the voltage higher than the what is should reach, which sets the supply to cc(current controled)
            PSU.set_source_ilim(1, 0)#set the max current we would want
            PSU.output_state(1, 'ON')#turn the output of the SMU
           

            print("before SOC")
            WRITER.writerow(["SOC"])
            measurment= take_soc()
            write_measurement(WRITER, measurment)
            print("\nafter SOC, before sweep")
            WRITER.writerow(["Current Sweep"])
            current_sweep(C, SIZE, WRITER)
            print('\nafter sweep, test done')
            WRITER.writerow(["End Test"])


            exit_all()
        except KeyboardInterrupt:
            exit_all() 


