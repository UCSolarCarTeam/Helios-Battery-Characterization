import numpy as np
import matplotlib.pyplot as plt
import scipy
import math as m
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any
import csv

np.random.seed(7)

current_sweep_i = np.linspace(0.2*c, 0.4*c, 50)
current_sweep_v = 0.5*np.random.randn(50)+3.6

current_pulse_i = []
for point in np.linspace(0.2*c, 0.4*c, 25):
    current_pulse_i.append(point)
    current_pulse_i.append(-1*point)

AC_response_i = []
x = np.linspace(0,4,100)
for i in x:
    AC_response_i.append(m.cos(i*2*m.pi))

y = 0.2*np.random.randn(100)+3.6
AC_response_v = []
AC_response_v_int = []
for i in x:
    AC_response_v_int.append(m.cos(i*2*m.pi - (m.pi/2)))
i = 0
while (i < 100):
    AC_response_v.append(AC_response_v_int[i]*y[i])
    i += 1

        return self.result

    def store_data(self):
        self.storage['current_pulse']['currentCP'] = self.get_current()
        self.storage['current_pulse']['voltageCP'] = self.get_voltage()
        self.storage['current_pulse']['resultCP'] = self.get_result()

AC_response_i = np.asarray(AC_response_i)
AC_response_v = np.asarray(AC_response_v)
x_data = np.asarray(x)



@dataclass
class ACResponse(Test):
    current_amplitude: float=1
    
    def get_voltage(self):
        v_init = []
        for i in np.linspace(0,1,self.size):
            v_init.append(m.cos(i*2*m.pi - (m.pi/2)))
        fake_voltage = 0.3*np.random.randn(self.size)+3.6
        i = 0
        while (i < self.size):
            self.voltage.append(v_init[i]*fake_voltage[i])
            i += 1

        return self.voltage

    def get_current(self):
        self.current = [(m.cos(point*2*m.pi)) for point in np.linspace(0,1,self.size)]
        self.current = [self.current_amplitude*point for point in self.current]

        return self.current

    def get_result(self):
        pass

    def store_data(self):
        self.storage['AC_response']['currentAC'] = self.get_current()
        self.storage['AC_response']['voltageAC'] = self.get_voltage()
        self.storage['AC_response']['resultAC'] = self.get_result()

        return self.storage

    def graph(self):
        voltage_array = np.asarray(self.get_voltage())
        current_array = np.asarray(self.get_current())
        x_data = np.asarray(np.linspace(0,1,self.size))

        
        #voltage fit
        guess =[3.6, 2*m.pi, m.pi/2]
        parameters, covariance = scipy.optimize.curve_fit(cos_func, x_data, voltage_array, p0=guess)
        fit_D = parameters[0]
        fit_E = parameters[1]
        fit_F = parameters[2]
        print(fit_D)
        print(fit_E)
        print(fit_F)
        fit_voltage = cos_func(x_data, fit_D, fit_E, fit_F)
        
        #plots
        ax1 = plt.subplot()
        ax1.plot(x_data, voltage_array, 'o', label = 'Voltage Response', color = 'blue')
        ax1.plot(x_data, fit_voltage, '-', label = 'Fit', color = 'blue')
        ax2 = ax1.twinx()
        ax2.plot(x_data, current_array, label = 'Input Current', color = 'red')
       
        #labels
        ax1.set_ylabel('Voltage V', c= 'blue')
        ax2.set_ylabel('Current A', c= 'red')
        ax2.spines['right'].set_color('red')
        ax2.spines['left'].set_color('blue')
        ax2.grid(c='red')
        ax2.tick_params(axis='y', colors='red')
        ax1.grid(c='blue')
        ax1.tick_params(axis='y', colors='blue')
        plt.show()

    



def cos_func(xdata, D, E, F):
    yx = D*(np.cos(E*xdata + F))
    return yx

cell_storage = {'SOC' : [],
           'AC_response' :{
                           'currentAC' : [],
                           'voltageAC' : [],
                           'resultAC' : []
                          },
            'current_pulse' :{
                           'currentCP' : [],
                           'voltageCP' : [],
                           'resultCP' : []
                          },
            'current_sweep' : {
                           'currentCS' : [],
                           'voltageCS' : [],
                           'resultCS' : []
                          },
          }



cell_number = 'test4-01-01'


SOC_test = SOC( current_c = 48000, voltage = [], current = [], storage = cell_storage, size = 6, result = [])
AC_test = ACResponse(current_c = 48000, voltage = [], current = [], storage = cell_storage, size = 6, result = [] )
CP_test = CurrentPulse(current_c = 48000, voltage = [], current = [], storage = cell_storage, size = 6, result = [] )
CS_test = CurrentSweep(current_c = 48000, voltage = [], current = [], storage = cell_storage, size = 6, result = [] )


SOC_test.store_data()
AC_test.store_data()
CP_test.store_data()
CS_test.store_data()

with open('test_carton.csv', 'a', newline='') as csvfile:
    fieldnames = ['cell #','SOC', 'voltageAC' , 'resultAC', 'voltageCP', 'resultCP', 'voltageCS', 'resultCS']

    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()


    row = {'cell #': cell_number,
            'SOC': SOC_test.voltage,
            'voltageAC': AC_test.voltage,
            'resultAC': AC_test.result,
            'voltageCP': CP_test.voltage,
            'resultCP': CP_test.result,
            'voltageCS': CS_test.voltage,
            'resultCS': CS_test.result 
        }

    writer.writerow(row)

    csvfile.close()

        










