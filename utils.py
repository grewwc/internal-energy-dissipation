from sympy import *
from numpy import e
from symbols import *





def Rj(u, v, w, p):
    s = Symbol('s')
    return 1.5 * integrate(1 / ((p + s) * sqrt((u + s) * (v + s) * (w + s))),
                           (s, 0, oo))


def get_theta(mode):
    if mode == 'L':
        return theta_max_L
    return theta_max_S


def get_B(mode='L'):
    if mode == 'L':
        return 1 - (1 - I22 / I11) * cos(theta_max_L)**2
    elif mode == 'S':
        return 1 - (1 - I22 / I33) * cos(theta_max_S)**2
    else:
        raise ValueError("wrong mode (L/S)")


def get_omega(mode='L'):
    if mode == 'L':
        return J * sqrt((1 / I11 - 1 / I22) * (get_B(mode) / I22 - 1 / I33))
    elif mode == 'S':
        return J * sqrt((1 / I22 - 1 / I33) * (1 / I11 - get_B(mode) / I22))
    else:
        raise ValueError("wrong mode (L/S)")


def get_k(mode='L'):
    if mode == 'L':
        return sin(get_theta(mode)) / sqrt(1 + cos(get_theta(mode)) *
                                           (1 / I11 - 1 / I22) /
                                           (1 / I22 - 1 / I33))
    elif mode == 'S':
        return sin(get_theta(mode)) / sqrt(1 + cos(get_theta(mode)) *
                                           (1 / I22 - 1 / I33) /
                                           (1 / I11 - 1 / I22))
    else:
        raise ValueError("wrong mode (L/S)")


# define sn, cn, dn


def sn(u, k, n):
    v = pi * u / (2 * K)
    return 2 * pi / (K * sqrt(k**2)) * sum([
        q**(i + 1 / 2) / (1 - q**(2 * i + 1)) * sin((2 * i + 1) * v)
        for i in range(n + 1)
    ])


def cn(u, k, n):
    v = pi * u / (2 * K)
    return 2 * pi / (K * sqrt(k**2)) * sum([
        q**(i + 1 / 2) / (1 + q**(2 * i + 1)) * cos((2 * i + 1) * v)
        for i in range(n + 1)
    ])


def dn(u, k, n):
    v = pi * u / (2 * K)
    return pi / (2 * K) + 2 * pi / K * sum(
        [q**i / (1 - q**(2 * i)) * cos((2 * i) * v) for i in range(1, n + 1)])


def get_F(mode='L'):
    if mode == 'L':
        return [
            dn(get_omega(mode), get_k(mode), 10),
            get_k(mode) * sn(get_omega(mode), get_k(mode), 10),
            cn(get_omega(mode), get_k(mode), 10)
        ]
    elif mode == 'S':
        return [
            cn(get_omega(mode), get_k(mode), 10),
            sn(get_omega(mode), get_k(mode), 10),
            dn(get_omega(mode), get_k(mode), 10)
        ]


def get_Omega(mode='L'):
    B = get_B(mode)
    F1, F2, F3 = get_F(mode)
    return [
        J / I11 * sqrt((B * I33 - I22) * I11 / ((I33 - I11) * I22)) * F1,
        J / I22 * sqrt((B * I33 - I22) / (I33 - I22)) * F2, 
        J / I33 * sqrt((I22 - B * I11) * I33 / ((I33 - I11) * I22)) * F3
    ]


def get_gamma():
    gamma1 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, 1)
    gamma2 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, h1**2)
    gamma3 = G*m/(a**3) * Rj(1, h1**2, h1**2*h2**2, h1**2*h2**2)
    return gamma1, gamma2, gamma3

def get_Bmat(Omega1, Omega2, Omega3, gamma1, gamma2, gamma3):
    Bmat = Matrix([
        [Omega2**2+Omega3**2-gamma1, -
            (2*Omega1*Omega2)/(1+h1**2), -(2*Omega1*Omega3)/(1+h1**2*h2**2)],
        [-(2*h1**2*Omega1*Omega2)/(1+h1**2), Omega1**2 +
        Omega3**2-gamma2, -(2*Omega1*Omega3)/(1+h2**2)],
        [-(2*h1**2*h2**2*Omega1*Omega3)/(1+h1**2*h2**2), -
        (2*h2**2*Omega1*Omega3)/(1+h2**2), Omega1**2+Omega2**2-gamma3]
    ])
    return Bmat


