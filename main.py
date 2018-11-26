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
        q0_x = (1 - t) * arr[0].x * arr[0].wx + t * arr[1].x * arr[1].wx
        q0_y = (1 - t) * arr[0].y * arr[0].wy + t * arr[1].y * arr[1].wy

        # q1 = (1-t) * p1 + t * p2
        q1_x = (1 - t) * arr[1].x * arr[1].wx + t * arr[2].x * arr[2].wx
        q1_y = (1 - t) * arr[1].y * arr[1].wy + t * arr[2].y * arr[2].wy

        # r = (1-t) * q0 + t * q1
        r_x = (1 - t) * q0_x + t * q1_x
        r_y = (1 - t) * q0_y + t * q1_y

        r = Point(expand(r_x), expand(r_y))
        return r

    else: # split array to two parts
        r0 = bezier_curve(arr[:-1])
        r1 = bezier_curve(arr[1:])

        # s = (1-t) * r0 + t * r1
        s_x = (1 - t) * r0.x * r0.wx + t * r1.x * r1.wx
        s_y = (1 - t) * r0.y * r0.wy + t * r1.y * r1.wy

        s = Point(expand(s_x), expand(s_y))
        return s


class Point:
    def __init__(self, x, y, wx=1, wy=1):
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy


def main():
    p0 = Point(1, 8)
    p1 = Point(-4, 2)
    p2 = Point(2, -4)
    p3 = Point(7, 1)
    p4 = Point(3, 3)

    e1 = Point(0, 0)
    e2 = Point(0, 6)
    e3 = Point(6, 6)
    e4 = Point(12, 0)

    r = bezier_curve([e1, e2, e3, e4])
    print((r.x, r.y))


if __name__ == '__main__':
    main()
