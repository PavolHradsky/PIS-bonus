import numpy as np
import matplotlib.pyplot as plt


def sigmoid_fuzzy_value(x, center, sigma):
    return 1 / (1 + np.exp(-((x - center) / sigma)))


def plot_sigmoid_fuzzy_value(range_start, range_end, measured_value, center, sigma, label):
    x = np.linspace(range_start, range_end, 1000)
    y = sigmoid_fuzzy_value(x, center, sigma)
    plt.plot(x, y, label=f'Center: {center}, Sigma: {sigma}')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=sigmoid_fuzzy_value(
        measured_value, center, sigma), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.show()


def obtain_sigmoid_fuzzy_value(measured_value, center, sigma):
    # call the function sigmoid_fuzzy_valuea and print the result
    sigmoid_value = sigmoid_fuzzy_value(measured_value, center, sigma)
    print(sigmoid_value)
    return sigmoid_value


def gaussian_fuzzy_value(x, center, sigma):
    return np.exp(-((x - center) ** 2) / (2 * sigma ** 2))


def obtain_gaussian_fuzzy_value(measured_value, center, sigma):
    # call the function gaussian_fuzzy_valuea and print the result
    gaussian_value = gaussian_fuzzy_value(measured_value, center, sigma)
    print(gaussian_value)
    return gaussian_value


def obtain_cup_gaussian_fuzzy_value(measured_value, center, sigma):
    # call the function gaussian_fuzzy_valuea and print the result
    gaussian_value = cup_gaussian_fuzzy_value(measured_value, center, sigma)
    print(gaussian_value)
    return gaussian_value


def cup_gaussian_fuzzy_value(x, center, sigma):
    return 1 - (1 - 0.1) * np.exp(-((x - center) ** 2) / (2 * sigma ** 2))


def plot_cup_gaussian_fuzzy_value(range_start, range_end, measured_value, center, sigma, label):
    x = np.linspace(range_start, range_end, 1000)
    y = cup_gaussian_fuzzy_value(x, center, sigma)
    plt.plot(x, y, label=f'Center: {center}, Sigma: {sigma}')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=cup_gaussian_fuzzy_value(
        measured_value, center, sigma), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.show()


print(plot_cup_gaussian_fuzzy_value(50, 200, 150, 165, 10, 'Cup Gaussian'))


class FuzzyPy():
    # Defines TRiangular membership finction f:x->y, with 'a' and 'c' the base of triangle and 'b' is peak
    def trimf(self, x, a, b, c):
        X1 = (x - a) / (b - a)
        X2 = (c - x) / (c - b)
        X3 = np.minimum(X1, X2)
        X4 = np.zeros(x.size)
        y = np.maximum(X3, X4)
        return y

    # Defines Trapezoidal membership finction f:x->y, with 'a' and 'd' the base of trpezoid and 'b' and 'c' the shoulder
    def trapmf(self, x, a, b, c, d):
        X1 = (x - a) / (b - a)
        X2 = np.ones(x.size)
        if d == c:
            X3 = np.ones(x.size)
        else:
            X3 = (d - x) / (d - c)
        X4 = np.minimum(np.minimum(X1, X2), X3)
        X5 = np.zeros(x.size)
        y = np.maximum(X4, X5)
        return y

    def gaussmf(self, x, c, v):
        """Compute Gaussian Membership function. """
        y = [np.exp(-np.power((i - c), 2) / (2 * v ** 2.0)) for i in x]
        return y


class Triangle(FuzzyPy):
    def __init__(self, x, low, middle, high):
        self.low = self.trimf(x, low[0], low[1], low[2])
        self.middle = self.trimf(x, middle[0], middle[1], middle[2])
        self.high = self.trimf(x, high[0], high[1], high[2])


class Triangle5(FuzzyPy):
    def __init__(self, x, low2, low1, middle, high1, high2):
        self.low2 = self.trimf(x, low2[0], low2[1], low2[2])
        self.low1 = self.trimf(x, low1[0], low1[1], low1[2])
        self.middle = self.trimf(x, middle[0], middle[1], middle[2])
        self.high1 = self.trimf(x, high1[0], high1[1], high1[2])
        self.high2 = self.trimf(x, high2[0], high2[1], high2[2])


class Trapezoid(FuzzyPy):
    def __init__(self, x, low, middle, high):
        self.low = self.trapmf(x, low[0], low[1], low[2], low[3])
        self.middle = self.trapmf(
            x, middle[0], middle[1], middle[2], middle[3])
        self.high = self.trapmf(x, high[0], high[1], high[2], high[3])


class Trapezoid5(FuzzyPy):
    def __init__(self, x, low2, low1, middle, high1, high2):
        self.low2 = self.trapmf(x, low2[0], low2[1], low2[2], low2[3])
        self.low1 = self.trapmf(x, low1[0], low1[1], low1[2], low1[3])
        self.middle = self.trapmf(
            x, middle[0], middle[1], middle[2], middle[3])
        self.high1 = self.trapmf(x, high1[0], high1[1], high1[2], high1[3])
        self.high2 = self.trapmf(x, high2[0], high2[1], high2[2], high2[3])


class Gauss(FuzzyPy):
    def __init__(self, x, low, middle, high):
        self.low = self.gaussmf(x, low[0], low[1])
        self.middle = self.gaussmf(x, middle[0], middle[1])
        self.high = self.gaussmf(x, high[0], high[1])


class Gauss5(FuzzyPy):
    def __init__(self, x, low2, low1, middle, high1, high2):
        self.low2 = self.gaussmf(x, low2[0], low2[1])
        self.low1 = self.gaussmf(x, low1[0], low1[1])
        self.middle = self.gaussmf(x, middle[0], middle[1])
        self.high1 = self.gaussmf(x, high1[0], high1[1])
        self.high2 = self.gaussmf(x, high2[0], high2[1])
#x = np.arange(0, 10, 0.1)


# Operators Defined

def intersect(A, B):
    """Intersect two membership functions"""
    return np.minimum(A, B)


def union(A, B):
    """Union of two membership functions"""
    return np.maximum(A, B)


def complement(A):
    """complement of membership"""
    return 1-A


def alphaCut(A, a):
    """Alpha cut on membership function"""
    from copy import deepcopy
    B = deepcopy(A)
    B[(B < a)] = 0
    return B


def add(A, B):
    """Adds two fuzzy membership functions/sets"""
    return np.minimum(A+B, 1)


def sub(A, B):
    """Subtracts two fuzzy membership functions/sets"""
    return np.maximum(A-B, 0)


def triangle_fuzzy_value(x, left, center, right):
    if x <= left or x >= right:
        return 0.0
    elif x == center:
        return 1.0
    elif x < center:
        return (x - left) / (center - left)
    else:
        return (right - x) / (right - center)


def obtain_triangular_fuzzy_value(measured_value, plot):
    triangular_value = triangle_fuzzy_value(
        measured_value, plot[0], plot[1], plot[2])
    print(triangular_value)
    return triangular_value


def draw_triangular_fuzzy_value(range_values, measured_value, left, center, right):
    value = Triangle(range_values, [left, center, right], [
                     left, center, right], [left, center, right])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Triangle')
    plt.axvline(x=measured_value, color='k')
    # plt.axhline(y=triangle_fuzzy_value(
    #    measured_value, left, center, right), color='k')
    plt.savefig('images_fuzzyfication/Triangle.png')
    plt.close()  # Close the plot window
# trapezoid fuzzy function


def trapezoid_fuzzy_value5(x, left1, left2, center, right1, right2):
    if x <= left2 or x >= right2:
        return 0.0
    elif x >= left1 and x <= right1:
        return 1.0
    elif x > left2 and x < left1:
        return (x - left2) / (left1 - left2)
    elif x > right1 and x < right2:
        return (right2 - x) / (right2 - right1)
    elif x > left1 and x < center:
        return 1.0
    else:
        return 1.0


def trapezoid_fuzzy_value(x, left, center_left, center_right, right):
    if x <= left or x >= right:
        return 0.0
    elif x >= center_left and x <= center_right:
        return 1.0
    elif x > left and x < center_left:
        return (x - left) / (center_left - left)
    else:
        return (right - x) / (right - center_right)


def obtain_trapezoid_fuzzy_value(measured_value, plot):
    if len(plot) == 4:
        trapezoid_value = trapezoid_fuzzy_value(
            measured_value, plot[0], plot[1], plot[2], plot[3])
    if len(plot) == 5:
        trapezoid_value = trapezoid_fuzzy_value5(
            measured_value, plot[0], plot[1], plot[2], plot[3], plot[4])

    print(trapezoid_value)
    return trapezoid_value


def draw_trapezoid_fuzzy_value(range_values, measured_value, low_plot, medium_plot, heigh_plot):
    value = Trapezoid(range_values, low_plot, medium_plot, heigh_plot)
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Trapezoid')
    plt.axvline(x=measured_value, color='k')
    #plt.axhline(y=obtain_trapezoid_fuzzy_value(measured_value), color='g')
    plt.savefig('images_fuzzyfication/Trapezoid.png')
    plt.close()  # Close the plot window
# gaussian fuzzy fuction


def draw_gaussian_fuzzy_value(range_values, measured_value, center, sigma):
    value = Gauss(range_values, [center, sigma], [
                  center, sigma], [center, sigma])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Gaussian')
    plt.axvline(x=measured_value, color='g')
    plt.axhline(y=gaussian_fuzzy_value(
        measured_value, center, sigma), color='g')
    plt.savefig('images_fuzzyfication/Gaussian.png')
    plt.close()  # Close the plot window
# sigmoid fuzzy function


def sigmoid_fuzzy_value(x, center, sigma):
    return 1 / (1 + np.exp(-((x - center) / sigma)))


def draw_sigmoid_fuzzy_value(range_values, measured_value, center, sigma):
    value = Gauss(range_values, [center, sigma], [
                  center, sigma], [center, sigma])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Sigmoid')
    plt.axvline(x=measured_value, color='g')
    plt.axhline(y=sigmoid_fuzzy_value(
        measured_value, center, sigma), color='g')
    plt.savefig('images_fuzzyfication/Sigmoid.png')
    plt.close()  # Close the plot window
