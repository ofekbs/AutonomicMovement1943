___Author___ = 'Ofek Bengal Shmueli'


from sympy import *  # <- For Bezier equations
import matplotlib.pyplot as plt
from Tkinter import *


# Constants
IS_2018_BOARD = True

TKINTER_SIZE = "400x300"  # in px
SIMULATOR_SIZE = (5, 5)  # 1 inch = 100px

V_MAX = 40  # Max velocity of the robot in cm/s
A_MAX = 1  # Max acceleration of the robot in cm/s^2

X_LEN = 823  # Length of x axis in simulator
Y_LEN = 823  # Length of y axis in simulator
POINT_SIZE = 5  # Size of a point in simulator
LINE_WIDTH = 2  # Width of a line in simulator
SAMPLE_SIZE = 1000


points = []
paths = []

fig = plt.figure(figsize=SIMULATOR_SIZE)
ax = fig.add_subplot(1, 1, 1, aspect=1)
ax.set_xlim(0, X_LEN)
ax.set_ylim(0, Y_LEN)
ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
ax.set_title("Spline Simulator", fontsize=10, verticalalignment='bottom')
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


def calc_value(expression, t_new):
    """
    I don't know how to say "Hatzava" in English, so deal with it.
    :param expression: parametric expression, usually p.x or p.y
    :param t_new: the value we won't to "Lehatziv" (god dammit)
    :return: The calculated value.
    """
    t = Symbol('t')
    return expression.evalf(subs={t: t_new})


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


def find_length(arr):
    """
    Calculates the length of the curve until each point.
    :param arr: the trajectory.
    :return: the same trajectory with length value for each point.
    """
    length = 0
    arr[0]['length'] = 0
    for i in range(len(arr)-1):
        x1 = calc_value(arr[i]['x'], i * 1.0 / SAMPLE_SIZE)
        x2 = calc_value(arr[i + 1]['x'], (i + 1) * 1.0 / SAMPLE_SIZE)
        y1 = calc_value(arr[i]['y'], i * 1.0 / SAMPLE_SIZE)
        y2 = calc_value(arr[i + 1]['y'], (i + 1) * 1.0 / SAMPLE_SIZE)
        length += sqrt((x2 - x1)**2 + (y2 - y1)**2)  # Distance
        arr[i+1]['length'] = length
    return arr


def physics(arr):
    """
    Does all the physics using the kinematics equations we all know and hate.
    :param arr: the trajectory.
    :return: the same trajectory with time, velocity and acceleration values for each point.
    """
    path_length = arr[len(arr)-1]['length']
    # If there was no velocity limit, how much time would it take to pass a half of the path at the max acceleration?
    # x = x0 + v0 * t + 0.5 * a * t^2
    # path_length/2 = 0 + 0 * t + 0.5 * A_MAX * t^2
    half_t = sqrt(path_length/A_MAX)

    # And how fast would we get at the end?
    # v = v0 + at
    # v = 0 + A_MAX * t
    no_limit_v = A_MAX * half_t

    # But, is it really possible to go this fast?
    if no_limit_v <= V_MAX:  # Yes! Run robot, run!
        # So, let's divide it into 2 parts.
        # In the first part, we will go at the max acceleration
        # In the second, we will go at the minus max acceleration, so we will stop exactly at the end of the path

        # But what point will be the last one to enter the first part?
        middle = 0
        for i in xrange(1, len(arr)):
            if arr[i]['length'] >= path_length / 2:
                middle = i - 1
                break

        # First part
        for i in range(middle+1):
            # x = x0 + v0 * t + 0.5 * a * t^2
            # x = 0 + 0 * t + 0.5 * A_MAX * t^2
            arr[i]['t'] = sqrt(2*arr[i]['length'] / A_MAX)
            # v = v0 + at
            # v = 0 + A_MAX * t
            arr[i]['v'] = A_MAX * arr[i]['t']
            # a = A_MAX
            arr[i]['a'] = A_MAX

        # Second part
        for i in range(middle+1, len(arr)):
            # x = x0 + v0 * t + 0.5 * a *t^2
            # x = path_length/2 + no_limit_v * (t - half_t) + 0.5 * (-A_MAX) * (t - half_t)^2
            t1 = (-2 * no_limit_v - 2 * A_MAX * half_t + 2 *
                  sqrt(no_limit_v ** 2 + 2 * A_MAX * path_length/2 - 2 * A_MAX * arr[i]['length'])) / (-2 * A_MAX)
            t2 = (-2 * no_limit_v - 2 * A_MAX * half_t - 2 *
                  sqrt(no_limit_v ** 2 + 2 * A_MAX * path_length/2 - 2 * A_MAX * arr[i]['length'])) / (-2 * A_MAX)

            # Oh no! Two solutions! Which one is correct?
            if not t1.is_real or t1 < 0 or t1 > 2 * half_t:  # No complex, negative or bigger numbers than the path
                                                            # time here!
                arr[i]['t'] = t2
            else:
                arr[i]['t'] = t1

            # v = v0 + at
            # v = no_limit_v + (-A_MAX) * (t - half_t)
            arr[i]['v'] = no_limit_v - A_MAX * (arr[i]['t'] - half_t)
            # a = -A_MAX
            arr[i]['a'] = -A_MAX

    else:  # No! You would stop at the max velocity!
        # So, let's divide it into 3 parts.
        # In the first part, we will go at the max acceleration until we reach the max velocity
        # In the second part, we will go at the same velocity - the max velocity
        # In the third, we will at the minus max acceleration, so we will stop exactly at the end of the path

        # When and where does the first part end?
        # v = v0 + at
        # V_MAX = 0 + A_MAX * part1_end_t
        part1_end_t = float(V_MAX) / A_MAX
        # x = x0 + v0 * t + 0.5 * a * t^2
        # part1_end_x = 0 + 0 * part1_end_t + 0.5 * A_MAX * part1_end_t^2
        part1_end_x = float(V_MAX ** 2) / (2 * A_MAX)

        # What point will be the last one to enter the first part?
        first_part = 0
        for i in xrange(1, len(arr)):
            if arr[i]['length'] >= part1_end_x:
                first_part = i - 1
                break

        # First part
        for i in range(first_part+1):
            # x = x0 + v0 * t + 0.5 * a * t^2
            # x = 0 + 0 * t + 0.5 * A_MAX * t^2
            arr[i]['t'] = sqrt(2 * arr[i]['length'] / A_MAX)
            # v = v0 + a * t
            # v = 0 + A_MAX * t
            arr[i]['v'] = A_MAX * arr[i]['t']
            # a = A_MAX
            arr[i]['a'] = A_MAX

        # Where and when does the second part end?
        # The third part's length is the same as the first, so we can calculate the second's length
        part2_end_x = path_length - part1_end_x
        # t * v = x
        # (part2_end_t - part1_end_t) * V_MAX = (part2_end_x - part1_end_x)
        part2_end_t = part1_end_t + (part2_end_x - part1_end_x) / V_MAX

        # What point will be the last one to enter the second part?
        second_part = 0
        for i in xrange(first_part, len(arr)):
            if arr[i]['length'] >= part2_end_x:
                second_part = i - 1
                break

        # Second part
        for i in range(first_part+1, second_part+1):
            # x = x0 + v0 * t
            # x = part1_end_x + V_MAX * (t - part1_end_t)
            arr[i]['t'] = part1_end_t + (arr[i]['length'] - part1_end_x) / V_MAX

            # v = V_MAX
            arr[i]['v'] = V_MAX

            # a = 0
            arr[i]['a'] = 0

        # Third part
        for i in range(second_part+1, len(arr)):
            # x = x0 + v0 * t + 0.5 * a * t^2
            # x = part2_end_x + V_MAX * (t - part2_end_t) + 0.5 * (-A_MAX) * (t - part2_end_t)^2
            t1 = (-2 * V_MAX - 2 * A_MAX * part2_end_t + 2 *
                  sqrt(V_MAX ** 2 + 2 * A_MAX * part2_end_x - 2 * A_MAX * arr[i]['length'])) / (-2 * A_MAX)
            t2 = (-2 * V_MAX - 2 * A_MAX * part2_end_t - 2 *
                  sqrt(V_MAX ** 2 + 2 * A_MAX * part2_end_x - 2 * A_MAX * arr[i]['length'])) / (-2 * A_MAX)

            # Oh no! Two solutions! Which one is correct?
            if not t1.is_real or t1 < 0 or t1 > part1_end_t + part2_end_t:  # No complex, negative or bigger numbers
                                                                            # than the path time here!
                arr[i]['t'] = t2
            else:
                arr[i]['t'] = t1

            # v = v0 + at
            # v = V_MAX + (-A_MAX) * (t - part2_end_t)
            arr[i]['v'] = V_MAX - A_MAX * (arr[i]['t'] - part2_end_t)

            # a = -A_MAX
            arr[i]['a'] = -A_MAX

# Tkinter functions


class Window(Frame):
    lines_count = 0

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.lines = None

    def init_window(self):
        self.master.title("Simulator manager")
        self.pack(fill=BOTH, expand=1)
        self.lines = []
        self.add_line()

    def add_line(self):
        if self.lines_count == 0:
            entry = Entry(self, text="", width=20)
            entry.grid(column=1, row=self.lines_count)
            btn_add = Button(self, text="Add", command=self.add_command)
            btn_add.grid(column=2, row=self.lines_count)
            label = Label(self, text=str(self.lines_count))
            label.grid(column=3, row=self.lines_count)

            self.lines.append((entry, btn_add))

            self.lines_count = self.lines_count + 1

        else:
            if self.lines[self.lines_count-1][0].get() == "":
                print("can't add another line")
            else:
                entry = Entry(self, text="", width=20)
                entry.grid(column=1, row=self.lines_count)
                btn_add = Button(self, text="Add", command=self.add_command)
                btn_add.grid(column=2, row=self.lines_count)
                label = Label(self, text=str(self.lines_count))
                label.grid(column=3, row=self.lines_count)

                self.lines.append((entry, btn_add))

                print(self.lines_count-1)

                com_to_execute = self.lines[self.lines_count-1][0].get()
                print(com_to_execute)
                execute(com_to_execute)

                self.lines_count = self.lines_count + 1

        print("created line " + str(self.lines_count-1))

    def add_command(self):
        self.add_line()


# Plot functions


def plot_2018_board():
    """
    Plot the 2018 board.
    see: https://firstfrc.blob.core.windows.net/frc2018/Manual/HTML/2018FRCGameSeasonManual_files/image008.jpg
    and: https://i.redd.it/3iwa9dircqd01.png
    for extra details.
    ***at the moment, only half scoring table is plotted.*
    """
    top_left_corner_border = plt.Polygon([[0,823], [91,823], [0,747]], fill='k', edgecolor='k')
    bottom_left_corner_border = plt.Polygon([[0,0], [0,76], [91,0]], fill='k', edgecolor='k')
    plt.gca().add_line(top_left_corner_border)
    plt.gca().add_line(bottom_left_corner_border)

    # Auto Line
    auto_line = plt.Line2D((305, 305), (0, 823), lw=2.5)
    plt.gca().add_line(auto_line)

    # Exchange Zone
    exchange_zone = plt.Rectangle((0, 442), 91, 122, fc='r')
    plt.gca().add_patch(exchange_zone)

    # Power Cube Zone
    power_cube_zone = plt.Rectangle((249, 354), 107, 114, fc='r')
    plt.gca().add_patch(power_cube_zone)

    # Switch Zone
    switch_zone = plt.Rectangle((356, 216), 142, 390, fc='grey')
    plt.gca().add_patch(switch_zone)

    # Power Cubes next to Switch Zone
    for i in range(0,6,1):
        cube = plt.Rectangle((498, 216+i*(33+38.4)), 33, 33, fc='yellow')
        plt.gca().add_patch(cube)

    # Null territory
    null_territory_top = plt.Polygon([[731.5, 581], [731.5, 823], [823, 823], [823, 581]], fill=None, edgecolor='k')
    null_territory_bottom = plt.Polygon([[731.5, 0], [731.5, 242], [823, 242], [823, 0]], fill=None, edgecolor='k')
    plt.gca().add_line(null_territory_top)
    plt.gca().add_line(null_territory_bottom)

    # Scale
    scale = plt.Rectangle((653.5, 242), 823-653.5, 581-242, fc='black')
    plt.gca().add_patch(scale)


def plot():
    arr = []
    for p in points:
        ax.plot(p.x, p.y, marker='o', label=str(p.name), linewidth=1, markersize=POINT_SIZE)

    for p in paths:
        x, y = curve_to_arrays(p, SAMPLE_SIZE, 1.0/SAMPLE_SIZE)
        ax.plot(x, y, 'r', linewidth=LINE_WIDTH)
        for i in range(len(x)):
            arr.append({'x': x[i], 'y': y[i]})
        arr = find_length(arr)
        physics(arr)

    if IS_2018_BOARD:
        plot_2018_board()

    plt.show()

    # Test graphs
    # v, t = [], []
    # for i in arr:
    #     v.append(i['v'])
    #     t.append(i['t'])
    # fig1, ax1 = plt.subplots()
    # ax1.plot(t, v, 'r', linewidth=LINE_WIDTH)

    print("plot ended")
    return "ok"


def execute(input):
    # Point => name = (x, y)
    # Path => name = a, b, ...

    print("executing: " + input)

    name, parameters = str(input).split(' = ')[0], str(input).split(' = ')[1]

    if parameters[:1] == '(': # New point
        if len(parameters[1:].split(',')) == 4:
            x = int(parameters[1:].split(',')[0])
            y = int(parameters[1:].split(',')[1])
            wx = int(parameters[1:].split(',')[2])
            wy = int(parameters[1:].split(',')[3][:-1])

            p = Point(x, y, wx, wy, name)

        else:
            x = int(parameters[1:].split(',')[0])
            y = int(parameters[1:].split(',')[1][:-1])

            p = Point(x, y, 1, 1, name)

        points.append(p)

    else:  # New path
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
    root.geometry(TKINTER_SIZE)
    app = Window(root)

    if IS_2018_BOARD:
        plot_2018_board()
    plt.show()

    # Test commands
    execute("a = (0,0)")
    execute("b = (200,800)")
    execute("c = (400,300)")
    execute("d = (200,200)")
    execute("p = a,b,c,d")

    root.mainloop()


if __name__ == '__main__':
    main()
