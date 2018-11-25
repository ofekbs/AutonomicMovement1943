import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.plotting import plot as p
from sympy import symbols

t = Symbol('t')

p0 = (1,2)
p1 = (10,5)
p2 = (8,9)

# q0 = (1-t) * p0 + t * p1
q0_x = (1-t) * p0[0] + t * p1[0]
q0_y = (1-t) * p0[1] + t * p1[1]

# q1 = (1-t) * p1 + t * p2
q1_x = (1-t) * p1[0] + t * p2[0]
q1_y = (1-t) * p1[1] + t * p2[1]

# r = (1-t) * q0 + t * q1
r_x = (1-t) * q0_x + t * q1_x
r_y = (1-t) * q0_y + t * q1_y

r = (expand(r_x), expand(r_y))
print(r)

x = symbols('x')
p(x**2, (x,-5,5))

#t = np.linspace(0, 1, 100)
#plt.plot(np.exp(r_x), np.exp(r_y))
#plt.ylabel('some numbers')
#plt.show()