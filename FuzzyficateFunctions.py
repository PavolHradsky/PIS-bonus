import numpy as np
import matplotlib.pyplot as plt


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


class Trapezoid(FuzzyPy):
    def __init__(self, x, low, middle, high):
        self.x = x
        self.low = self.trapmf(x, low[0], low[1], low[2], low[3])
        self.middle = self.trapmf(
            x, middle[0], middle[1], middle[2], middle[3])
        self.high = self.trapmf(x, high[0], high[1], high[2], high[3])


class Gauss(FuzzyPy):
    def __init__(self, x, low, middle, high):
        self.low = self.gaussmf(x, low[0], low[1])
        self.middle = self.gaussmf(x, middle[0], middle[1])
        self.high = self.gaussmf(x, high[0], high[1])

#x = np.arange(0, 10, 0.1)


def triangle_fuzzy_value(x, left, center, right):
    if x <= left or x >= right:
        return 0.0
    elif x == center:
        return 1.0
    elif x < center:
        return (x - left) / (center - left)
    else:
        return (right - x) / (right - center)


def obtain_triangular_fuzzy_value(measured_value, left, center, right):
    triangular_value = triangle_fuzzy_value(
        measured_value, left, center, right)
    print(triangular_value)
    return triangular_value


def draw_triangular_fuzzy_value(range_values, measured_value, left, center, right):
    value = Triangle(range_values, [left, center, right], [
                     left, center, right], [left, center, right])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Triangle')
    plt.axvline(x=measured_value, color='r')
    plt.axhline(y=triangle_fuzzy_value(
        measured_value, left, center, right), color='g')
    plt.legend()
    plt.show()
# trapezoid fuzzy function


def trapezoid_fuzzy_value(x, left, center_left, center_right, right):
    if x <= left or x >= right:
        return 0.0
    elif x >= center_left and x <= center_right:
        return 1.0
    elif x > left and x < center_left:
        return (x - left) / (center_left - left)
    else:
        return (right - x) / (right - center_right)


def obtain_trapezoid_fuzzy_value(measured_value, left, center_left, center_right, right):
    trapezoid_value = trapezoid_fuzzy_value(
        measured_value, left, center_left, center_right, right)
    print(trapezoid_value)
    return trapezoid_value


def draw_trapezoid_fuzzy_value(range_values, measured_value, left, center_left, center_right, right):
    value = Trapezoid(range_values, [left, center_left, center_right, right], [left, center_left, center_right, right],
                      [left, center_left, center_right, right])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Trapezoid')
    plt.axvline(x=measured_value, color='r')
    plt.axhline(y=trapezoid_fuzzy_value(measured_value, left,
                center_left, center_right, right), color='g')
    plt.legend()
    plt.show()


# gaussian fuzzy fuction
def gaussian_fuzzy_value(x, center, sigma):
    return np.exp(-((x - center) ** 2) / (2 * sigma ** 2))


def obtain_gaussian_fuzzy_value(measured_value, center, sigma):
    # call the function gaussian_fuzzy_valuea and print the result
    gaussian_value = gaussian_fuzzy_value(measured_value, center, sigma)
    print(gaussian_value)
    return gaussian_value


def draw_gaussian_fuzzy_value(range_values, measured_value, center, sigma):
    value = Gauss(range_values, [center, sigma], [
                  center, sigma], [center, sigma])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Gaussian')
    plt.axvline(x=measured_value, color='r')
    plt.axhline(y=gaussian_fuzzy_value(
        measured_value, center, sigma), color='g')
    plt.legend()
    plt.show()

# sigmoid fuzzy function


def sigmoid_fuzzy_value(x, center, sigma):
    return 1 / (1 + np.exp(-((x - center) / sigma)))


def obtain_sigmoid_fuzzy_value(measured_value, center, sigma):
    # call the function sigmoid_fuzzy_valuea and print the result
    sigmoid_value = sigmoid_fuzzy_value(measured_value, center, sigma)
    print(sigmoid_value)
    return sigmoid_value


def draw_sigmoid_fuzzy_value(range_values, measured_value, center, sigma):
    value = Gauss(range_values, [center, sigma], [
                  center, sigma], [center, sigma])
    plt.plot(range_values, value.low, 'b', linewidth=1.5, label='low')
    plt.plot(range_values, value.middle, 'g', linewidth=1.5, label='middle')
    plt.plot(range_values, value.high, 'r', linewidth=1.5, label='high')
    plt.title('Sigmoid')
    plt.axvline(x=measured_value, color='r')
    plt.axhline(y=sigmoid_fuzzy_value(
        measured_value, center, sigma), color='g')
    plt.legend()
    plt.show()
