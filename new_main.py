___Author___ = 'Ofek Bengal Shmueli'


from sympy import *  # <- For Bezier equations
import matplotlib.pyplot as plt
from tkinter import *


X_LEN = 15 # Length of x axis
Y_LEN = 15 # Length of y axis
POINT_SIZE = 5
LINE_WIDTH = 2
points = []
paths = []

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(1, 1, 1, aspect=1)
ax.set_xlim(0, X_LEN)
ax.set_ylim(0, Y_LEN)
ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
ax.set_title("Spline Simulator", fontsize=10, verticalalignment='bottom')
ax.legend()
plt.ion()


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

    for i in range(0, n, 1):
        x_list.append(calc_value(p.x, 0 + i * d))
        y_list.append(calc_value(p.y, 0 + i * d))

    return x_list, y_list


# Tkinter functions


class Window(Frame):
    lines_count = 0

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()


    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        self.lines = []
        self.add_line()

    def add_line(self):
        if self.lines_count == 0:
            entry = Entry(self, text="", width=20)
            entry.grid(column=1, row=self.lines_count)
            btnAdd = Button(self, text="Add", command = self.add_command)
            btnAdd.grid(column=2, row=self.lines_count)
            label = Label(self, text=str(self.lines_count))
            label.grid(column=3, row=self.lines_count)

            self.lines.append((entry, btnAdd))

            self.lines_count = self.lines_count + 1

        else:
            if self.lines[self.lines_count-1][0].get() == "":
                print("can't add another line")
            else:
                entry = Entry(self, text="", width=20)
                entry.grid(column=1, row=self.lines_count)
                btnAdd = Button(self, text="Add", command=self.add_command)
                btnAdd.grid(column=2, row=self.lines_count)
                label = Label(self, text=str(self.lines_count))
                label.grid(column=3, row=self.lines_count)
                self.lines.append((entry, btnAdd))

                print(self.lines_count-1)

                com_to_execute = self.lines[self.lines_count-1][0].get()
                print(com_to_execute)
                ok = execute(com_to_execute)

                self.lines_count = self.lines_count + 1

        print("created line " + str(self.lines_count-1))

    def add_command(self):
        self.add_line()


# Plot functions


def plot():

    for p in points:
        ax.plot(p.x, p.y, marker='o', label=str(p.name), linewidth=1, markersize=5)

    for p in paths:
        x, y = curve_to_arrays(p, 500, 1/500)
        ax.plot(x, y, 'r--', linewidth=10)

    plt.show()

    print("plot ended")
    return "ok"




def execute(input):
    # Point => name = (x, y)
    # Path => name = a, b, ...

    print("executing: " + input)

    name, parameters = str(input).split(' = ')[0], str(input).split(' = ')[1]

    if parameters[:1] == '(':
        x = int(parameters[1:].split(',')[0])
        y = int(parameters[1:].split(',')[1][:-1])

        p = Point(x, y, 1, 1, name)
        points.append(p)

    else:
        requested = parameters.split(',')
        send = []

        for r in requested:
            for p in points:
                if p.name == r:
                    send.append(p)

        curve = bezier_curve(send)
        paths.append(curve)

    if plot() == "ok":
        print("execute ended")
        return "ok"

# Main function


def main():
    root = Tk()
    root.geometry("400x300")
    app = Window(root)

    plt.show()

    #ax.plot(3, 5, marker='o', label="hello", linestyle='dashed', linewidth=2, markersize=5)

    root.mainloop()


if __name__ == '__main__':
    main()