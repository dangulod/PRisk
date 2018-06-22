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


def linear(x1, x2, y1, y2, x):
    m = (y1 - y2) / (x1 - x2)
    y = (x - x2) * m + y2
    return y


class Curve:
    def __init__(self, name, base,
                 days, rates,
                 compounding=compounded,
                 interpolator=linear):
        self.name = name
        self.base = base
        self.days = days
        self.rates = rates
        self.tenors = self.days.size
        self.compounding = compounding
        self.interpolator = interpolator

    def __str__(self):
        return "Curve: " + self.name + ", base: " + self.base + ", with " + str(self.tenors) + " tenors"

    def rate(self, t):
        pos = which(self.days, t)
        if (pos == 0): return self.rates[0]

        return self.interpolator(self.days[pos - 1],
                                 self.days[pos],
                                 self.rates[pos - 1],
                                 self.rates[pos],
                                 t)

    def discount(self, t):
        pos = which(self.days, t)
        d = t / 365
        return 1 / (self.compounding(self.rate(t), 1) ** d)