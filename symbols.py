from sympy import *
names = {
    'Omega': chr(937),
    'nv': chr(957),
    'omega': chr(969),
}
# constatns

Omega1 = Symbol("Omega1")
Omega2 = Symbol("Omega2")
Omega3 = Symbol("Omega3")

gamma1 = Symbol("gamma1")    
gamma2 = Symbol("gamma2")
gamma3 = Symbol("gamma3")


h1 = Symbol('h1', constant=True)
h2 = Symbol('h2', constant=True)
h3 = Symbol('h3', constant=True)

G = Symbol('G', constant=True)
m = Symbol('m', constant=True)
a = Symbol('a', constant=True)

I11 = Symbol('I11', constant=True)
I22 = Symbol('I22', constant=True)
I33 = Symbol('I33', constant=True)

J = Symbol("J", constant=True)
Tkin = Symbol("Tkin", constant=True)

t = Symbol('t')

theta_max_L = Symbol('theta_max_L')
theta_max_S = Symbol('theta_max_S')

k, nv = symbols('k {}'.format(names['nv']))

x,y,z = symbols('x y z')

K = elliptic_k(k**2)
K_ = elliptic_k(1 - k**2)
q = exp(-pi * K_ / K)
