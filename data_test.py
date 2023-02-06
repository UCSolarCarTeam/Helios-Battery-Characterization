import numpy as np
import pandas as pd
import math as m

c = 4800
np.random.seed(7)

current_sweep_i = np.linspace(0.2*c, 0.4*c, 50)
current_sweep_v = 0.5*np.random.randn(50)+3.6

current_pulse_i = []
for point in np.linspace(0.2*c, 0.4*c, 25):
    current_pulse_i.append(point)
    current_pulse_i.append(-1*point)

AC_response_i = []
x = np.linspace(0,49,50)
for i in x:
    AC_response_i.append(m.cos(1000*i))

print(AC_response_i)





