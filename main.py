import math as m
import scipy.special
from sympy import *


def bezier(i, n, t):
    return binomial(n, i) * pow(t, i) * pow(1 - t, n - i)


def bezier_curve(arr):
    t = Symbol('t')
    x = 0
    y = 0
    n = len(arr) - 1 # highest degree

    for i in range(0, n + 1, 1):
        x = x + bezier(i, n, t) * arr[i].x
        y = y + bezier(i, n, t) * arr[i].y

    return Point(expand(x), expand(y))


def derivative(arr):
    t = Symbol('t')
    x = 0
    y = 0
    n = len(arr) - 1

    for i in range(0, n, 1):
        x = x + bezier(i, n - 1, t) * (arr[i + 1].x - arr[i].x)
        y = y + bezier(i, n - 1, t) * (arr[i + 1].y - arr[i].y)

    return Point(expand(x), expand(y))


def rational_bezier_curve(arr):
    t = Symbol('t')
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    n = len(arr) - 1  # highest degree

    for i in range(0, n + 1, 1):
        x1 = x1 + bezier(i, n, t) * arr[i].x * arr[i].wx
        x2 = x2 + bezier(i, n, t) * arr[i].wx
        y1 = y1 + bezier(i, n, t) * arr[i].y * arr[i].wy
        y2 = y2 + bezier(i, n, t) * arr[i].wy

    x = expand(x1) / expand(x2)
    y = expand(y1) / expand(y2)

    return Point(expand(x), expand(y))


class Point:
    def __init__(self, x, y, wx=1, wy=1):
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy

    def to_string(self):
        x = str(self.x).replace("**", "^")
        y = str(self.y).replace("**", "^")

        return str("("+x+", "+y+")")


class Control_Points:
    def __init__(self, points):
        self.points = points

    def to_string(self):
        for i in range(0, len(self.points), 1):
            print("Point " + str(i) + ": " + self.points[i].to_string)


def main():
    p0 = Point(0,0)
    p1 = Point(3, 10, 5, 5)
    p2 = Point(6, 3)
    p3 = Point(10, 7)
    p4 = Point(13, 5, 5, 5)
    p5 = Point(10, 3)

    cp = Control_Points([p0, p1])

    p = bezier_curve(cp.points)
    print(p.to_string())

    p_der = derivative(cp.points)
    print(p_der.to_string())

    p_rat = rational_bezier_curve(cp.points)
    print(p_rat.to_string())


if __name__ == '__main__':
    main()