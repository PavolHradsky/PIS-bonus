import numpy as np
import matplotlib.pyplot as plt


def sigmoid_fuzzy_value(x, center, sigma):
    return 1 / (1 + np.exp(-((x - center) / sigma)))


def plot_sigmoid_fuzzy_value(range_start, range_end, measured_value, center, sigma, label):
    x = np.linspace(range_start, range_end, 1000)
    y = sigmoid_fuzzy_value(x, center, sigma)
    plt.plot(x, y, label=f'Center: {center}, Sigma: {sigma}')
    plt.legend()
    plt.xlabel('Measured Value')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=sigmoid_fuzzy_value(
        measured_value, center, sigma), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.clf()


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
    return gaussian_value


def obtain_cup_gaussian_fuzzy_value(measured_value, center, sigma):
    # call the function gaussian_fuzzy_valuea and print the result
    gaussian_value = cup_gaussian_fuzzy_value(measured_value, center, sigma)
    return gaussian_value


def cup_gaussian_fuzzy_value(x, center, sigma):
    return 1 - (1 - 0.1) * np.exp(-((x - center) ** 2) / (2 * sigma ** 2))


def plot_cup_gaussian_fuzzy_value(range_start, range_end, measured_value, center, sigma, label):
    x = np.linspace(range_start, range_end, 1000)
    y = cup_gaussian_fuzzy_value(x, center, sigma)
    plt.plot(x, y, label=f'Center: {center}, Sigma: {sigma}')
    plt.legend()
    plt.xlabel('Measured Value')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=cup_gaussian_fuzzy_value(
        measured_value, center, sigma), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.clf()


def trapezoid_fuzzy_value_5(x, a, b, c, d):
    X1 = (x - a) / (b - a)
    X2 = (d - x) / (d - c)
    X3 = np.minimum(X1, X2)
    X4 = np.zeros(x.size)
    y = np.maximum(X3, X4)
    return y


def plot_trapezoid_fuzzy_value_5(range_start, range_end, measured_value, a, b, c, d, label):
    x = np.linspace(range_start, range_end, 1000)
    y = trapezoid_fuzzy_value_5(x, a, b, c, d)
    plt.plot(x, y, label=f'a: {a}, b: {b}, c: {c}, d: {d}')
    plt.legend()
    plt.xlabel('Measured Value')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=trapezoid_fuzzy_value_5(
        measured_value, a, b, c, d), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.clf()


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
    trapezoid_value = trapezoid_fuzzy_value(
        measured_value, plot[0], plot[1], plot[2], plot[3])
    return trapezoid_value


def plot_trapezoid_fuzzy_value(range_start, range_end, measured_value, a, b, c, d, label):
    x = np.linspace(range_start, range_end, 1000)
    y = [trapezoid_fuzzy_value(xi, a, b, c, d) for xi in x]
    plt.plot(x, y, label=f'a: {a}, b: {b}, c: {c}, d: {d}')
    plt.legend()
    plt.xlabel('Measured Value')
    plt.ylabel('Fuzzy Value')
    plt.title(label)
    plt.axvline(x=measured_value, color='k')
    plt.axhline(y=trapezoid_fuzzy_value(measured_value, a, b, c, d), color='k')
    plt.savefig('images_fuzzyfication/'+label+'.png')
    plt.clf()
