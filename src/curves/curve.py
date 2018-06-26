from math import exp
import numpy as np


def simple(r, t):
    return (1 + r * t)


def compounded(r, t):
    return (1 + r) ** t


def continuous(r, t):
    return exp(r * t)


def which(x, a):  # assert 'x' np.array & 'a' int
    for i in range(0, len(x)):
        if (x[i] > a): return i


# Interpolator

def splines(x, y, new_days):

    from scipy.interpolate import CubicSpline

    CS= CubicSpline(x, y)
    return CS(new_days)


def linear(x, y, x0):
    pos = which(x, x0)

    if ( pos == 0 ): return x[0]

    y1 = y[pos - 1]
    y2 = y[pos]
    x1 = x[pos - 1]
    x2 = x[pos]

    m = (y1 - y2) / (x1 - x2)
    y0 = (x - x2) * m + y2
    return y0


class Curve:
    def __init__(self, name, days, rates,
                 compounding=compounded,
                 interpolator=linear):
        self.name = name
        self.days = days
        self.rates = rates
        self.compounding = compounding
        self.interpolator = interpolator

    def rate(self, Date):
        pos = which(self.days, Date)
        if (pos == 0): return self.rates[0]

        return self.interpolator(self.days,
                                 self.rates,
                                 Date)

    def discount(self, t):
        d = t / 365
        return 1 / (self.compounding(self.rate(t), 1) ** d)

if __name__ == "__main__":

    from src.dates.date import Date, Days

    valDate = Date(31, 12, 2017)
    days = [valDate + Days(180), valDate + Days(360), valDate + Days(720), valDate + Days(1080),
            valDate + Days(1800), valDate + Days(2520), valDate + Days(3600)]

    rates = np.array([-0.00326, -0.00382, -0.00172, -0.00035,
                      0.00401, 0.01029, 0.01908])

    PT_BOND = Curve("PT_BOND", days, rates)

    print(PT_BOND.rate(Date(31, 1, 2019)))
