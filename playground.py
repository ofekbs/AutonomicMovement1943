import math as m
import scipy.special
from sympy import *


def binom(n, k):
    return scipy.special.binom(n, k)


def bezier(n):
    t = Symbol('t') # Equation's var.

    s = 0
    for i in range(0, n, 1):
        b = binom(n, i)
        m1 = m.pow(1-t, n-i)
        m2 = m.pow(t, i)

        s = s + b * m1 * m2
    return s


def main():
    print(bezier(2))


if __name__ == '__main__':
    main()