from sympy import *
from numpy import e

from symbols import *

subs = False


def Rj(u, v, w, p):
    s = Symbol('s')
    return 1.5*integrate(1/((p+s)*sqrt((u+s)*(v+s)*(w+s))), (s, 0, oo))


def get_theta(mode):
    if mode == 'L':
        return theta_max_L
    return theta_max_S


def get_B(mode='L'):
    if mode == 'L':
        return 1 - (1-I22/I11)*cos(theta_max_L) ** 2
    elif mode == 'S':
        return 1 - (1-I22/I33)*cos(theta_max_S) ** 2
    else:
        raise ValueError("wrong mode (L/S)")


def get_omega(mode='L'):
    if mode == 'L':
        return J * sqrt((1/I11-1/I22)*(get_B(mode)/I22-1/I33))
    elif mode == 'S':
        return J * sqrt((1/I22-1/I33)*(1/I11-get_B(mode)/I22))
    else:
        raise ValueError("wrong mode (L/S)")


def get_k(mode='L'):
    if mode == 'L':
        return sin(get_theta(mode)) / sqrt(1+cos(get_theta(mode)) * (1/I11-1/I22)/(1/I22-1/I33))
    elif mode == 'S':
        return sin(get_theta(mode)) / sqrt(1+cos(get_theta(mode)) * (1/I22-1/I33)/(1/I11-1/I22))
    else:
        raise ValueError("wrong mode (L/S)")



print(get_B)
