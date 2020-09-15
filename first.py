from sympy import * 


x, y = symbols('x y')

y = x**2

print(y)

print(y.subs({x: sin(x)}))