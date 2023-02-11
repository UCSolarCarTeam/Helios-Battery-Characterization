import numpy as np
import matplotlib.pyplot as plt
import scipy
import math as m
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any

c = 4800

np.random.seed(7)

@dataclass
class Test(ABC):
    current_c: int
    voltage: list[Any]
    current: list[Any]
    storage: dict
    size: int
    result: list[Any]

    @abstractmethod
    def get_voltage(self):
        ...

    @abstractmethod
    def get_current(self):
        ...

    @abstractmethod
    def get_result(self):
        ...

@dataclass
class CurrentSweep(Test):

    def get_voltage(self)-> list:
        self.voltage = list(0.5*np.random.randn(self.size)+3.6)
        
        return self.voltage

    def get_current(self)-> list:
        self.current =list(np.linspace(0.2*self.current_c, 0.4*self.current_c, self.size))

        return self.current

    def get_result(self):
        i = 0
        while (i < self.size):
            self.result.append(self.voltage[i]/self.current[i])
            i += 1

        return self.result

    
    def store_data(self):
        self.storage['current_sweep']['current'] = self.get_current()
        self.storage['current_sweep']['voltage'] = self.get_voltage()
        self.storage['current_sweep']['result'] = self.get_result()


        return self.storage

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
            self.result.append(self.get_voltage()[i]/self.get_current()[i])
            i += 1

        return self.result

    def store_data(self):
        self.storage['current_pulse']['current'] = self.get_current()
        self.storage['current_pulse']['voltage'] = self.get_voltage()
        self.storage['current_pulse']['result'] = self.get_result()

        return self.storage
        


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
        self.storage['AC_response']['current'] = self.get_current()
        self.storage['AC_response']['voltage'] = self.get_voltage()
        self.storage['AC_response']['result'] = self.get_result()

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
                           'current' : [],
                           'voltage' : [],
                           'result' : []
                          },
            'current_pulse' :{
                           'current' : [],
                           'voltage' : [],
                           'result' : []
                          },
            'current_sweep' : {
                           'current' : [],
                           'voltage' : [],
                           'result' : []
                          },
          }

carton_storage = [cell_storage for point in range(130)]


test = ACResponse(current_c = 48000, voltage = [], current = [], storage = carton_storage[0], size = 50, result = [] )
test2 = CurrentPulse(current_c = 48000, voltage = [], current = [], storage = carton_storage[0], size = 6, result = [] )
test3 = CurrentSweep(current_c = 48000, voltage = [], current = [], storage = carton_storage[0], size = 6, result = [] )





#storage['AC_response']['current'] = [1,2,3,4]

#print(storage['AC_response']['current'])
'''test.store_data()
test2.store_data()
test3.store_data()

print(test.graph())'''

test.graph()










