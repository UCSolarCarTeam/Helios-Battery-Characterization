import numpy as np
import matplotlib.pyplot as plt
import scipy
import math as m

c = 4800
np.random.seed(7)

current_sweep_i = np.linspace(0.2*c, 0.4*c, 50) #Makes current range
current_sweep_v = 0.5*np.random.randn(50)+3.6 #Makes voltage values

current_pulse_i = []
for point in np.linspace(0.2*c, 0.4*c, 25):
    current_pulse_i.append(point)
    current_pulse_i.append(-1*point) #makes the a varying current pulse

AC_response_i = []
x = np.linspace(0,4,100) #number of samples
for i in x:
    AC_response_i.append(m.cos(i*2*m.pi)) #Creates an AC response current

y = 0.2*np.random.randn(100)+3.6 # voltage amplitudes
AC_response_v = []
AC_response_v_int = []
for i in x:
    AC_response_v_int.append(m.cos(i*2*m.pi - (m.pi/2))) #Creates AC voltage sinusoid, voltage leads current by pi/2
i = 0
while (i < 100):
    AC_response_v.append(AC_response_v_int[i]*y[i]) #Creates voltage sinusoid
    i += 1


AC_response_i = np.asarray(AC_response_i) #Converts AC_response_i into an np array
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





