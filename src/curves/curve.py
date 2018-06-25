from math import exp
import numpy as np


def simple(r, t):
    return (1 + r * t)


def compounded(r, t):
    return (1 + r) ** t


def continuous(r, t):
    return exp(r * t)


def which(x, a):  # assert 'x' np.array & 'a' int
    for i in np.arange(x.size):
        if (x[i] > a): return i


# Interpolator

def splines(x, y, new_days):

    from scipy.interpolate import CubicSpline

    CS= CubicSpline(x, y)
    return CS(new_days)

def linear(x1, x2, y1, y2, x):
    m = (y1 - y2) / (x1 - x2)
    y = (x - x2) * m + y2
    return y


class Curve:
    def __init__(self, name, days, rates,
                 compounding=compounded,
                 interpolator=linear):
        self.name = name
        self.days = days
        self.rates = rates
        self.compounding = compounding
        self.interpolator = interpolator

    def rate(self, t):
        pos = which(self.days, t)
        if (pos == 0): return self.rates[0]

        return self.interpolator(self.days[pos - 1],
                                 self.days[pos],
                                 self.rates[pos - 1],
                                 self.rates[pos],
                                 t)

    def discount(self, t):
        d = t / 365
        return 1 / (self.compounding(self.rate(t), 1) ** d)

if __name__ == "__main__":

    days = np.array([180, 360, 720, 1080,
                     1800, 2520, 3600])

    rates = np.array([-0.00326, -0.00382, -0.00172, -0.00035,
                      0.00401, 0.01029, 0.01908])

    PT_BOND = Curve("PT_BOND", days, rates)

    print(PT_BOND.rate(90))
