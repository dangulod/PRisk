from src.dates.date import Date, Days, Weeks, Months, Quarters, Semesters, Years
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
import numpy as np

class Product:
    def __init__(self):
        pass

    def NPV(self, val_date):
        pass

class Bond(Product):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, fix_flo, calendar = Calendar()):
        self.nominal      = nominal
        self.startDate    = startDate
        self.matDate      = matDate
        self.base         = base
        self.curve_irr    = curve_irr
        self.curve_spread = curve_spread
        self.coupon       = coupon,
        self.c_frequency  = c_frequency
        self.fix_flo      = fix_flo
        self.calendar     = calendar

    def couponsDate(self):
        pass

    def couponsPayment(self):
        pass

    def NPV(self, val_date):
        return self.nominal


class BondInf(Bond):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, fix_flo, day, IPCA, IPCA_p, calendar = Brazil()):
        super(BondInf, self).__init__(nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, fix_flo, calendar = calendar)
        self.day    = day
        self.IPCA   = IPCA
        self.IPCA_p = IPCA_p

    def NPV(self, val_date):
        return self.nominal


class Equity(Product):
    def __init__(self, nominal, factor):
        self.nominal = nominal
        self.factor = factor

    def NPV(self, val_date):
        return self.nominal * self.factor


class Cash(Product):
    def __init__(self, value):
        self.value = value

    def NPV(self, val_date):
        return self.value


class Portfolio:
    def __init__(self):
        pass

    def append(self, p):
        if ( not isinstance(p, Product) ):
            raise ValueError("p must be a Product")
        try:
            self.products.append(p)
        except AttributeError:
            self.products = [p]

    def NPV(self, val_date):
        value = 0
        for i in self.products:
            value += i.NPV(val_date)
        return value


if __name__ == "__main__":

    carter = Portfolio()

    carter.append(Bond(nominal = 1, startDate = Date( 3, 4, 2015), matDate = Date(30, 7, 2030,),
                       base = "ACT/ACT", curve_irr = "ES_BOND", curve_spread = "iBoxx",
                       coupon = 0.0178246127679505, c_frequency = 1, fix_flo = True)
                  )

    carter.append(Bond(nominal = 2, startDate = Date(16,10, 2105), matDate = Date(31,10, 2044),
                       base = "ACT/ACT", curve_irr = "ES_BOND", curve_spread = "iBoxx",
                       coupon = 0.0223354303582122, c_frequency  = 1, fix_flo = True)
                  )

    carter.append(BondInf(nominal = 1000, startDate = Date(15, 5, 2015), matDate = Date(15, 5, 2015),
                          base = "BUSS/252", curve_irr = "BR_BOND", curve_spread = "iBoxx", coupon = 0,
                          c_frequency = 1, fix_flo = True, day = 15, IPCA = 1.532670225, IPCA_p = 1))

    carter.append(Cash(3))

    print(carter.NPV(Date(29,12, 2012)))

