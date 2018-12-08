___Author___ = 'Ofek Bengal Shmueli'


from sympy import *  # <- For Bezier equations
import threading
import pygame
import pygame.locals
import time

surf = None
points = []
lines = []
points_x = []
points_y = []


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

    x = x1 / x2
    y = y1 / y2

    return Point(x, y)


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

    for i in xrange(n):
        x_list.append(calc_value(p.x, 0 + i * d))
        y_list.append(calc_value(p.y, 0 + i * d))

    return x_list, y_list


def add_point(point):
    """
    A function that adds a point. Can you believe that??
    :param point: a point.
    """
    name, cor = point.split(' ')[0], point[len(point.split(' ')[0]):]
    x, y = cor.split(',')[0], cor.split(',')[1]
    points.append(Point(int(x), int(y), 1, 1, name))
    points_x.append(int(x))
    points_y.append(int(y))

    print("point added.")


def draw_path(string):
    """
    Draws a path between given control points.
    :param string: the control points.
    """
    global lines
    requested = string.split(',')
    send = []

    for r in requested:
        for p in points:
            if p.name == r:
                send.append(p)

    before = time.time()
    p = bezier_curve(send)
    x, y = curve_to_arrays(p, 100, 0.01)
    lines = []
    for i in xrange(len(x)):
        lines.append((x[i], y[i]))
    lines.append((send[-1].x, send[-1].y))
    print 'Time taken: ' + str(time.time() - before) + ' seconds'


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


# Functions related to visual issues, pygame, plotting, etc.

def wait_for_command():
    add_point('a 2,3')
    add_point('b 5,1')
    add_point('c 4,4')
    add_point('d 8,2')
    add_point('e 1,3')

    while True:
        command = raw_input(">> ")
        if command.split(' ')[0] == "help":
            helper()
        if command.split(' ')[0] == "np":
            add_point(command[3:])
        if command.split(' ')[0] == "dp":
            draw_path(command[3:])
        if command.split(' ')[0] == "sp":
            show_points()
        if command.split(' ')[0] == "exit":
            exit()


def main():
    global surf
    #pygame.init()
    #surf = pygame.display.set_mode((600, 600))
    #pygame.display.set_caption("Bezier Curves!")

    wait_for_command()
    threading.Thread(target=wait_for_command).start()

    while True:
        surf.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i in points:
            pygame.draw.circle(surf, (255, 0, 0), (i.x, i.y), 5)
        for i in xrange(len(lines)-1):
            pygame.draw.line(surf, (0, 0, 0), lines[i], lines[i+1], 3)
        pygame.display.update()


if __name__ == '__main__':
    main()
