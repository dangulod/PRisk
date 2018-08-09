from math import exp
from src.utils.utils import which, where
from src.dates.date import Date, Periods
from src.utils.getters import get_base
from src.dates.calendar import Calendar
import numpy as np

def simple(r, t):
    return (1 + r * t)


def compounded(r, t):
    return (1 + r) ** t


def continuous(r, t):
    return exp(r * t)

# Interpolator

def splines(x, y, x0):

    from scipy.interpolate import CubicSpline

    return CubicSpline(x, y, x0) # Revisar si esta bien


def linear(x, y, x0):
    if isinstance(x0, (float, Date)):
        return [linearInterpol(x, y, x0)]

    vector = [0] * len(x0)

    for i in range(0, len(x0)):
        vector[i] = linearInterpol(x, y, x0[i])

    return vector


def linearInterpol(x, y, x0):
    if x0 >= x[len(x) - 1]: return y[len(x) - 1]

    pos = which(x, x0)

    if ( pos == 0 ): return y[0]

    y1 = y[pos - 1]
    y2 = y[pos]
    x1 = x[pos - 1]
    x2 = x[pos]

    m = (y2 - y1) / (x2 - x1)
    y0 = (x0 - x1) * m + y1
    return y0


class Curve:
    def __init__(self, name, dates, rates, compounding=compounded, base="ACT/365",
                 interpolator=linear, calendar=Calendar()):
        if len(dates) != len(rates):
            raise ValueError("Dates and Rates must have the same length")
        if not isinstance(dates, list):
            raise ValueError("Dates must be a list")
        if not isinstance(rates, list):
            raise ValueError("Rates must be a list")
        self.name  = name
        self.dates = dates
        self.rates = rates
        self.base  = get_base(base)
        self.compounding  = compounding
        self.interpolator = interpolator
        self.calendar = calendar

    def __str__(self):
        return str(self.name) + " " + str(len(self.dates)) + " tenors"

    def __repr__(self):
        return str(self.name) + " " + str(len(self.dates)) + " tenors"

    def __len__(self):
        return len(self.rates)

    def __add__(self, other):
        if isinstance(other, float):
            l = len(self)
            dates = [0] * l
            rates = [0] * l
            for i in range(0, l):
                dates[i] = self.dates[i]
                rates[i] = self.rates[i] + other
            x = Curve(name=self.name, dates=dates, rates=rates, compounding=self.compounding,
                      interpolator=self.interpolator, calendar=self.calendar)
            x.base = self.base
            return x
        if isinstance(other, Curve):
            dates = list(np.unique(self.dates + other.dates))
            l     = len(dates)
            rates = [0] * l
            r1    = self.rate(dates)
            r2    = other.rate(dates)

            for i in range(0, l):
                rates[i] = r1[i] + r2[i]

            curva = Curve(name=self.name + "+" + other.name,
                          dates=dates,
                          rates=rates,
                          interpolator=self.interpolator,
                          compounding=self.compounding,
                          calendar=self.calendar)
            curva.base = self.base
            return curva
        if isinstance(other, NullCurve):
            return self

    def rate(self, Date):
        return self.interpolator(self.dates,
                                 self.rates,
                                 Date)

    def simple_forward(self, val_date: Date, t1: Date, t2: Date):
        '''
        Simple compounding is used for the forward rate
        '''
        ft1 = self.discount(val_date=val_date, date=t1)[0]
        ft2 = self.discount(val_date=val_date, date=t2)[0]
        yf  = self.base.yearFraction(d1=t1, d2=t2, calendar=self.calendar)

        return ((ft1 / ft2) - 1) / yf

    def compounded_forward(self, val_date: Date, t1: Date, t2: Date):
        '''
        Compounded compounding is used for the forward rate
        '''
        ft1 = self.discount(val_date=val_date, date=t1)[0]
        ft2 = self.discount(val_date=val_date, date=t2)[0]
        yf  = self.base.yearFraction(d1=t1, d2=t2, calendar=self.calendar)

        return ((ft1 / ft2)) ** (1 / yf) - 1

    def continuous_forward(self, val_date: Date, t1: Date, t2: Date):
        '''
        Compounded compounding is used for the forward rate
        '''
        ft1 = self.rate(Date=t1)[0]
        ft2 = self.rate(Date=t2)[0]
        y1  = self.base.dayCount(d1=val_date, d2=t1, calendar=self.calendar)
        y2  = self.base.dayCount(d1=val_date, d2=t2, calendar=self.calendar)
        yff = self.base.dayCount(d1=t1, d2=t2, calendar=self.calendar)

        return (ft2 * y2 - ft1 * y1) / yff

    def FWD(self, val_date: Date, t: Periods):
        l = len(self)
        fwds = [0] * l

        for i in range(0, l):
            d = self.base.yearFraction(val_date + t, self.dates[i] + t, calendar=self.calendar)
            dd1 = self.discount(val_date, val_date + t)[0]
            dd2 = self.discount(val_date, self.dates[i] + t )[0]
            fwds[i] = (dd1 / dd2) ** (1 / d) - 1

        return fwds

    def discount(self, val_date: Date, date: Date):
        rates = self.rate(date)
        l = len(date)
        dis = [0] * l
        if isinstance(date, Date): date = [date]

        for i in range(0, l):
            dis[i] = 1 / (self.compounding(rates[i], 1) ** self.base.yearFraction(val_date, date[i], self.calendar))

        return dis


class NullCurve(Curve):
    def __init__(self):
        self.name  = ""
        self.dates = []

    def __str__(self):
        return "NullCurve"

    def __repr__(self):
        return "NullCurve"

    def rate(self, Date):
        return [0] * len(Date)

    def discount(self, val_date, date):
        return 1

class IRR(Curve):
    def __init__(self, irr):
        self.irr = irr
        self.name = ""
        self.dates = []

    def rate(self, Date):
        return [self.irr] * len(Date)

    def __add__(self, other):
        if isinstance(other, NullCurve):
            return self

def get_curve(name, array):
    if ( name == "None" ):
        return NullCurve()
    try:
        return array[where(array.map(lambda x: x.name), name)]
    except ValueError:
        raise ValueError("curve %s not found" % name)


def copy_curve(curve_from: Curve):
    l = len(curve_from)
    dates = curve_from.dates
    name = curve_from.name
    rates = [0] * l
    for i in range(0, l):
        rates[i] = curve_from.rates[i]
    x = Curve(name, dates, rates, compounding=curve_from.compounding, interpolator=curve_from.interpolator)
    x.base = curve_from.base
    return x


if __name__ == "__main__":

    from src.dates.date import Date, Days, Years

    valDate = Date(31, 12, 2017)

    days = [valDate + Days(180), valDate + Days(360), valDate + Days(720), valDate + Days(1080),
            valDate + Days(1800), valDate + Days(2520), valDate + Days(3600)]

    rates = [-0.00326, -0.00382, -0.00172, -0.00035,
              0.00401, 0.01029, 0.01908]

    days1 = [valDate + Days(180), valDate + Days(365), valDate + Days(725), valDate + Days(1080),
            valDate + Days(1800), valDate + Days(2525), valDate + Days(3600)]

    rates1 = [-0.00326, -0.00382, -0.00172, -0.00035,
             0.00401, 0.01029, 0.01908]

    PT_BOND = Curve("PT_BOND", days, rates)
    ES_BOND = Curve("ES_BOND", days1, rates1)

    import numpy as np

    print(np.unique(PT_BOND.dates + ES_BOND.dates))

    print((PT_BOND + ES_BOND).rates)

    print(PT_BOND.simple_forward(valDate, Date(31, 12, 2018), Date(31, 12, 2020)))
    print(PT_BOND.compounded_forward(valDate, Date(31, 12, 2018), Date(31, 12, 2020)))
    print(PT_BOND.continuous_forward(valDate, Date(31, 12, 2018), Date(31, 12, 2020)))
    print(PT_BOND.FWD(valDate, t=Years(1)))

    print((PT_BOND + IRR(0.1)).rates)
    print((PT_BOND + NullCurve()).rates)
    #print(PT_BOND.rate([valDate + Days(20), Date(31, 1, 2020)]))
    #print(PT_BOND.discount(valDate, Date(31, 1, 2020)))

