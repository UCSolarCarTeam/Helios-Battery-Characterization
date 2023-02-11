import numpy as np
import matplotlib.pyplot as plt
import scipy
import math as m
from dataclasses import dataclass
from abc import ABC, abstractmethod

c = 4800
np.random.seed(7)
@dataclass
class Test(ABC):
    current_c: int
    voltage: Any
    current: list[Any]
    storage: dict{Any}
    size: int
    result: list[]

    def store_data(self):
        self.storage['current_sweep']['current'] = self.current
        self.storage['current_sweep']['voltage'] = self.voltage

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

    def get_voltage(self):
        self.voltage = 0.5*np.random.randn(50)+3.6

    def get_current(self):
        self.current =list(np.linspace(0.2*self.current_c, 0.4*self.current_c, self.size))

    def get_result(self):
        i = 0
        while (i < self.size):
            self.result.append = (self.voltage[i]/self.current[i])

@dataclass
class CurrentPulse(Test):

    def get_volatge(self):
        pass

    def get_current(self):
        for point in np.linspace(0.2*self.current_c, 0.4*self.current_c, int((self.size)/2)):
            self.current.append(point)
            self.current.append(-1*point)
    
    def get_result(self):
        i = 0
        while (i < self.size):
            self.result.append = (self.voltage[i]/self.current[i])
        


@dataclass
class ACResponse(Test):
    current_amplitude: float=1
    
    def get_voltage(self):
        AC_response_v_int = []
        for i in np.linspace(0,4,self.size):
            AC_response_v_int.append(m.cos(i*2*m.pi - (m.pi/2)))
        i = 0
        while (i < self.size):
            self.voltage.append(AC_response_v_int[i]*y[i])
            i += 1

    def get_current(self):
        self.current = [(m.cos(point*2*m.pi)) for point in np.linspace(0,4,self.size)]
        self.current = [self.current_amplitude*point for point in self.current]

    def get_result(self):
        pass

        
        
    


AC_response_i = np.asarray(AC_response_i)
AC_response_v = np.asarray(AC_response_v)
x_data = np.asarray(x)



def cos_func(xdata, D, E, F):
    yx = D*(np.cos(E*xdata + F))
    return yx

guess =[3.6, 2*m.pi, m.pi/2]
parameters, covariance = scipy.optimize.curve_fit(cos_func, x_data, AC_response_v, p0=guess)
fit_D = parameters[0]
fit_E = parameters[1]
fit_F = parameters[2]
print(fit_D)
print(fit_E)
print(fit_F)

fit_yx = cos_func(x_data, fit_D, fit_E, fit_F)

ax1 = plt.subplot()
ax1.plot(x_data, AC_response_v, 'o', label = 'Voltage Response', color = 'blue')
ax1.plot(x_data, fit_yx, '-', label = 'Fit', color = 'blue')
#plt.plot(x_data, AC_response_v, 'o', label = 'data')
ax2 = ax1.twinx()
ax2.plot(x_data, AC_response_i, label = 'Input Current', color = 'red')
#plt.plot(x_data, AC_response_i, label = 'Current')
#plt.plot(x_data, fit_yx, '-', label = 'fit')
ax1.set_ylabel('Voltage V', c= 'blue')
ax2.set_ylabel('Current A', c= 'red')
ax2.spines['right'].set_color('red')
ax2.spines['left'].set_color('blue')
ax2.grid(c='red')
ax2.tick_params(axis='y', colors='red')
ax1.grid(c='blue')
ax1.tick_params(axis='y', colors='blue')
plt.show()






storage = {'SOC' : [],
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



