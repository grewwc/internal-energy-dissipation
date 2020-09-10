from sympy import *
from utils import * 
import numpy as np

from symbols import * 


def Rj(u, v, w, p):
    return 1.5 * integrate()




Omega1 = Symbol("Omega1")
Omega2 = Symbol("Omega2")
Omega3 = Symbol("Omega3")

gamma1 = Symbol("gamma1")    
gamma2 = Symbol("gamma2")
gamma3 = Symbol("gamma3")


if subs:
    gamma1 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, 1)
    gamma2 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, h1**2)
    gamma3 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, h1**2*h2**2)



Bmat = Matrix([
    [Omega2**2+Omega3**2-gamma1, -
        (2*Omega1*Omega2)/(1+h1**2), -(2*Omega1*Omega3)/(1+h1**2*h2**2)],
    [-(2*h1**2*Omega1*Omega2)/(1+h1**2), Omega1**2 +
     Omega3**2-gamma2, -(2*Omega1*Omega3)/(1+h2**2)],
    [-(2*h1**2*h2**2*Omega1*Omega3)/(1+h1**2*h2**2), -
     (2*h2**2*Omega1*Omega3)/(1+h2**2), Omega1**2+Omega2**2-gamma3]
])



print(Bmat)