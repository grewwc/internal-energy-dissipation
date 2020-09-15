from sympy import *
from symbols import *
import sympy


class Argument(Symbol):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr__(self, other):
        return str(self)


t = Symbol('t')
x = Symbol('x')
y = x ** 2

x = sqrt(t)

print('free', y.subs())
print(y.base)
temp = y.subs(x, sqrt(t))
print(sympify(temp))
res = integrate(temp, t)
print(res)
