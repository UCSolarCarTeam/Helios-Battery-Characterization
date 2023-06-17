import numpy as np
import matplotlib.pyplot as plt
import scipy
import math as m
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any
import csv

np.random.seed(7)

@dataclass
class Test(ABC):
    voltage: list[Any]
    current: list[Any]
    storage: dict
    size: int
    result: list[Any]
    current_c: float = 4.800

    @abstractmethod
    def get_voltage(self):
        ...



@dataclass
class SOC(Test):

    def get_voltage(self) -> list:
        self.voltage = [3.5]
        return self.voltage
    
    def store_data(self):
        self.storage['SOC'] = self.get_voltage()

        return self.storage

@dataclass
class CurrentSweep(Test):

    def get_voltage(self)-> list:
        self.voltage = list(np.linspace(0.2*3.6, 0.4*3.6, self.size))
        
        return self.voltage

    def get_current(self)-> list:
        self.current =list(abs(np.linspace(0.2*self.current_c, 0.4*self.current_c, self.size)))


        return self.current

    def get_result(self):
        i = 0
        while (i < self.size):
            self.result.append(self.voltage[i]/self.current[i])
            i += 1

        return self.result

    
    def store_data(self):
        self.storage['current_sweep']['currentCS'] = self.get_current()
        self.storage['current_sweep']['voltageCS'] = self.get_voltage()
        self.storage['current_sweep']['resultCS'] = self.get_result()


        return self.storage
    
    def graph(self):
        result_array = np.asarray(self.result)
        voltage_array = np.asarray(self.voltage)
        current_array = np.asarray(self.get_current())

        plt.plot(result_array, c= 'green')
        plt.plot(voltage_array, c='blue')
        plt.plot(current_array,c='red')
        plt.show()
        

@dataclass
class CurrentPulse(Test):

    def get_voltage(self):
        self.voltage = list(0.3*np.random.randn(self.size)+3.6)

        return self.voltage

    def get_current(self):
        for point in np.linspace(0.2*self.current_c, 0.4*self.current_c, int((self.size)/2)):
            self.current.append(point)
            self.current.append(-1*point)

        return self.current
    
    def get_result(self):
        i = 0
        while (i < self.size-1 ):
            self.result.append(np.asarray(self.voltage)[i]/np.asarray(self.get_current()[i]))
            i += 1

        return self.result

    def store_data(self):
        self.storage['current_pulse']['currentCP'] = self.get_current()
        self.storage['current_pulse']['voltageCP'] = self.get_voltage()
        self.storage['current_pulse']['resultCP'] = self.get_result()

        return self.storage
    
    def graph(self):
        result_array = np.asarray(self.result)
        voltage_array = np.asarray(self.voltage)
        current_array = np.asarray(self.get_current())

        plt.plot(result_array, c= 'green')
        plt.plot(voltage_array, c='blue')
        plt.plot(current_array,c='red')
        plt.show()
        


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
        voltage_array = np.asarray(self.voltage)
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

def run_test(cell_number):


    SOC_test = SOC( current_c = 4800, voltage = [], current = [], storage = cell_storage, size = 100, result = [])
    AC_test = ACResponse(current_c = 4800, voltage = [], current = [], storage = cell_storage, size = 100, result = [] )
    CP_test = CurrentPulse(current_c = 4800, voltage = [], current = [], storage = cell_storage, size = 100, result = [] )
    CS_test = CurrentSweep(current_c = 4800, voltage = [], current = [], storage = cell_storage, size = 100, result = [] )

    with open('AC_current.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for point in AC_test.get_current():
            writer.writerow(["{:.2f}".format(point)])

    SOC_test.store_data()
    AC_test.store_data()
    CP_test.store_data()
    CS_test.store_data()

    with open('test_carton1.csv', 'a', newline='') as csvfile:
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

    
   


def reread_test(cell_number):
    with open('test_carton1.csv', 'r',  newline='') as csvfile:
    # Create a DictReader object for the CSV file
        reader = csv.DictReader(csvfile)

    
    # Iterate through the rows of the CSV file and print each row
        for row in reader:
            if row['cell #'] == cell_number:
                SOC = row['SOC']
                voltageAC = row['voltageAC']
                resultAC = row['resultAC']
                voltageCP = row['voltageCP']
                resultCP = row['resultCP']
                voltageCS = row['voltageCS']
                resultCS = row['resultCS']

                break

       
        
        punctuations = [',', ']', '[']

        for punctuation in punctuations:
            voltageAC = voltageAC.replace(punctuation, ' ')
            resultCP = resultCP.replace(punctuation, '')
            resultCS = resultCS.replace(punctuation, '')
            voltageCP = voltageCP.replace(punctuation, '')
            voltageCS = voltageCS.replace(punctuation, '')
    

        
        voltageAC = voltageAC.split()
        resultCP = resultCP.split()
        resultCS = resultCS.split()
        voltageCP = voltageCP.split()
        voltageCS = voltageCS.split()

        for i in range(len(voltageAC)):
            voltageAC[i] = float(voltageAC[i])

            
        for i in range(len(resultCP)):
            resultCP[i] = float(resultCP[i])

        for i in range(len(resultCS)):
            resultCS[i] = float(resultCS[i])

        for i in range(len(voltageCS)):
            voltageCS[i] = float(voltageCS[i])

        for i in range(len(voltageCS)):
            voltageCS[i] = float(voltageCS[i])



        AC_graph =  ACResponse(current_c = 4.800, voltage = voltageAC, current = [], storage = cell_storage, size = 100, result = [] )
        CP_graph = CurrentPulse(current_c = 4.800, voltage = voltageCP, current = [], storage = cell_storage, size = 100, result = resultCP ) 
        CS_graph = CurrentPulse(current_c = 4.800, voltage = voltageCS, current = [], storage = cell_storage, size = 100, result = resultCS ) 

        AC_graph.graph()
        CP_graph.graph()
        CS_graph.graph()
        

#run_test( 'test3-01-01')

reread_test('test3-01-01')



















