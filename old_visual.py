___Author___ = 'Ofek Bengal Shmueli'


from sympy import *  # <- For Bezier equations
import sys, pygame  # <- For the visual part
from pygame.locals import *  # <- Same
import matplotlib.backends.backend_agg as agg  # <- For plotting
import pylab  # <- Same
import matplotlib as plt


gameDisplay = pygame.display.set_mode((400, 400), DOUBLEBUF)

points = []
points_x = []
points_y = []
pygame.init()

screen = pygame.display.get_surface()
pygame.display.set_caption("Graph is loading, please wait...")
pygame.display.set_caption("Spline Generator - Live plot mode")


# Class definitions for Points and Control Points


class Point:
    """
    A point, defined by numbers of parameters.
    """
    def __init__(self, x, y, wx=1, wy=1, name=""):
        """
        :param x: x value
        :param y: y value
        :param wx: x weight. Default: 1 (no extra weight)
        :param wy: y weight. Default: 1 (no extra weight)
        :param name: point's name (optional)
        """
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy
        self.name = name

    def to_string(self):
        """
        Details about this point.
        :return: string with details
        """
        x = str(self.x).replace("**", "^")
        y = str(self.y).replace("**", "^")

        if self.name == "":
            return str("("+x+", "+y+")")
        else:
            return str(self.name+"("+x+", "+y+")")


# Functions related to Bezier, using math libs, etc.


def bezier(i, n, t):
    """
    The core of the Bezier formula.
    :param i: from for loop.
    :param n: highest degree of the curve.
    :param t: curve parameter.
    :return: b(t), see formula docs on Wikipedia.
    """
    return binomial(n, i) * pow(t, i) * pow(1 - t, n - i)


def bezier_curve(arr):
    """
    Calculates general point (Locus) of the curve, considers weights.
    :param arr: collection of points.
    :return: Locus of the curve (with weights).
    """
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


def der(p):
    t = Symbol('t')
    return diff(p.x, t), diff(p.y, t)


def calc_value(exp, t_new):
    """
    I don't know how to say "Hatzava" in English, so deal with it.
    :param exp: parametric expression, usually p.x or p.y
    :param t_new: the value we won't to "Lehatziv" (god dammit)
    :return: The calculated value.
    """
    t = Symbol('t')
    return exp.evalf(subs={t: t_new})


def curve_to_arrays(p, n, d):
    """
    Takes the general point and samples it into arrays.
    :param p: a general point.
    :param n: number of points we want.
    :param d: the distance between each point.
    :return: array with sampled points.
    """
    x_list = []
    y_list = []

    for i in range(0, n, 1):
        x_list.append(calc_value(p.x, 0 + i * d))
        y_list.append(calc_value(p.y, 0 + i * d))

    return x_list, y_list


# Functions related to visual issues, pygame, plotting, etc.


def update_canvas(code, point = Point(0,0)):
    """
    I don't know what this function actually does, but I don't care.
    :param code: np / dp
    :param point: for dp, general point to draw
    """
    fig = pylab.figure(figsize=[4, 4], dpi=100)
    ax = fig.gca()

    if code == "np": # new point
        ax.plot(points_x, points_y, 'ro')

    if code == "dp": # draw path
        ax.plot(points_x, points_y, 'ro')
        x, y = curve_to_arrays(point, 1000, 0.001)
        ax.plot(x, y, 'r--')

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()

    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    return ax


def add_point(point):
    """
    A function that adds a point. Can you believe that??
    :param point: a point.
    """

    if len(point.split(' ')) == 2:
        name, cor, wx, wy = point.split(' ')[0], point.split(' ')[1], 1, 1

    else:
        name, cor, wx, wy = point.split(' ')[0], point.split(' ')[1], point.split(' ')[2], point.split(' ')[3]

    x, y = cor.split(',')[0], cor.split(',')[1]

    points.append(Point(int(x),int(y), int(wx), int(wy), name))
    points_x.append(int(x))
    points_y.append(int(y))
    update_canvas("np")

    print("New point added.")


def draw_path(str):
    """
    Draws a path between given control points.
    :param str: the control points.
    """
    requested = str.split(',')
    send = []

    for r in requested:
        for p in points:
            if p.name == r:
                send.append(p)

    p = bezier_curve(send)
    update_canvas("dp", p)

    print("Path " + str + " drawn.")
    print(p.to_string())

    speed_x, speed_y = der(p)

    print(speed_x)
    print(speed_y)

    axel_x, axel_y = der(Point(speed_x, speed_y))

    print(axel_x)
    print(axel_y)



def show_points():
    """
    Prints points' details.
    """
    for x in points:
        print(x.to_string())


def helper():
    """
    None of your buisness.
    """
    print("USE THE FOLLOWING COMMANDS:")
    print("np - Creates new point.")
    print("\tnp point_name x, y")
    print("dp - Draw a path.")
    print("\tdp p0, p1, p2,...")
    print("sp - Show all points.")
    print("\tsp")
    print("help - Get this screen.")
    print("\thelp")
    print("exit - Exit the program.")
    print("\texit")

# Main function


def main():
    update_canvas("")
    print("\nSPLINE GENERATOR for #1943\n")

    crashed = False
    while not crashed:
        command = input(">> ")
        if command.split(' ')[0] == "help":
            helper()
        if command.split(' ')[0] == "np":
            add_point(command[3:])
        if command.split(' ')[0] == "dp":
            draw_path(command[3:])
        if command.split(' ')[0] == "sp":
            show_points()
        if command.split(' ')[0] == "exit":
            crashed = True


if __name__ == '__main__':
    main()