import sys
from time import time, sleep
from datetime import datetime
from PPH_1503D import PPH_1503D
import math as m 
import csv
import numpy as np

def take_measurement(stdout_suppressed=False):
    volt_samp = PSU.read_DVM()
    curr_samp = PSU.measure_current(1)

    # Print measurement
    if not stdout_suppressed:
        sys.stdout.write(f'\rBattery Voltage: {volt_samp} V, Battery Current: {curr_samp} A')
        sys.stdout.flush()

    return {"Batt_Volt": volt_samp,
            "Batt_Curr": curr_samp
            }

def write_measurement(file_handler, measurement):
    file_handler.writerow([datetime.now().strftime("%d-%m-%Y %H:%M:%S"), measurement["Batt_Volt"], measurement["Batt_Curr"]])
    sys.stdout.write('    *Logged')

def take_soc(stdout_suppressed=False):
    volt_samp = PSU.read_DVM()

    # Print measurement
    if not stdout_suppressed:
        sys.stdout.write(f'\rBattery Voltage: {volt_samp} V')
        sys.stdout.flush()

    return {"Batt_Volt": volt_samp,
            }

def current_sweep(current_c,size ):
    current =list(abs(np.linspace(0.2*current_c, 0.4*current_c, size)))
    currentsweep_update_int = 1.25
    currentsweep_measure_int = 1.25
    t_ref_update = time()
    t_ref_measurement = time()

    
        
    for data in current:
        t_ref_int_update = time()
        t_ref_int_measurement = time()

        if (t_ref_int_update - t_ref_update) >= currentsweep_update_int:  # timing for updates
            t_ref_update = t_ref_int_update
            PSU.set_source_ilim(1, data)
            measurement = take_measurement()

        if (t_ref_int_measurement - t_ref_measurement) >= currentsweep_measure_int:  # timing for measurements
            t_ref_measurement = t_ref_int_measurement
            measurement=take_measurement()
            write_measurement(file_handler=WRITER, measurement=measurement)

def ac_impedance(current_c, size):
    ac_impedance_current = [(m.cos(point*2*m.pi)) for point in np.linspace(0,1,size)]
    ac_impedance_update_int = 1.25
    ac_impedance_measure_int = 1.25
    t_ref_update = time()
    t_ref_measurement = time()   

    for i in range(0,1,1):
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
                write_measurement(file_handler=WRITER, measurement=measurement)
     
    
            



def exit_all():
    print('PSU output disabled - exiting.')
    PSU.output_state(1, 'OFF')
    PSU.__del__()
    exit()


if __name__ == "__main__":
    # Setup
    PSU = PPH_1503D('USB0::0x2184::0x002C::GEQ837356::3::INSTR')
    PSU.set_outp_ovp(1, 4.6)
    PSU.set_outp_ovp_state(1, 'ON')
    PSU.set_data_format('SREal')
    PSU.set_sense_func(1, 'VOl')
    PSU.set_sense_period(1, 1)
    PSU.set_sense_averaging(1, 10)

        # Test parameters
       # Interval between log writes in seconds

    CHARGE_V = 4.4
    CHARGE_I = 0.75              # 0.5 Cmin
    CHARGE_TERM_I = 0.03         # 0.02 Cmin
    DISCHARGE_I = -0.075         # 0.04 Cmin
    DISCHARGE_TERM_V = 3.0

    # Log setup 
    FILENAME = f'Cycle Test, Ichg={CHARGE_I}, Idschg={DISCHARGE_I}.csv'
    with open(FILENAME, 'w', newline='') as F:
        try:
            WRITER = csv.writer(F)   
        except KeyboardInterrupt:
            exit_all() 