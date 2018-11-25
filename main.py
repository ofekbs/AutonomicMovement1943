__Author__ = "Ofek BS"

from sympy import *


def bezier_curve(arr):
    """
    Creates a spline, using the Bezier Curve.
    :param arr: array of control points, sorted by x value.
                first and last point are fixed.
    :return: a general point - f(t).
    """

    t = Symbol('t') # Equation's var.

    if len(arr) == 3:
        # q0 = (1-t) * p0 + t * p1
        q0_x = (1 - t) * arr[0][0] + t * arr[1][0]
        q0_y = (1 - t) * arr[0][1] + t * arr[1][1]

        # q1 = (1-t) * p1 + t * p2
        q1_x = (1 - t) * arr[1][0] + t * arr[2][0]
        q1_y = (1 - t) * arr[1][1] + t * arr[2][1]

        # r = (1-t) * q0 + t * q1
        r_x = (1 - t) * q0_x + t * q1_x
        r_y = (1 - t) * q0_y + t * q1_y

        r = (expand(r_x), expand(r_y)) # remove brackets

        return r

    else: # split array to two parts
        r0 = bezier_curve(arr[:-1])
        r1 = bezier_curve(arr[1:])

        # s = (1-t) * r0 + t * r1
        s_x = (1 - t) * r0[0] + t * r1[0]
        s_y = (1 - t) * r0[1] + t * r1[1]

        s = (expand(s_x), expand(s_y))
        return s


def main():
    p0 = (1, 6)
    p1 = (3, 13)
    p2 = (6, 9)
    p3 = (10, 18)
    p4 = (12, 14)
    p5 = (16, 9)

    r = bezier_curve([p0, p1, p2])
    print(r)

if __name__ == '__main__':
    main()
