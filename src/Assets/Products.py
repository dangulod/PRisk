from src.dates.date import Date, Days, Weeks, Months, Quarters, Semesters, Years
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil

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
        self.c_frequency  = int(12 / c_frequency)
        self.fix_flo      = fix_flo
        self.calendar     = calendar

    def couponPayment(self, val_date):
        if (val_date > self.matDate): return 0
        i = 1
        coup = [self.matDate]
        while (( self.matDate - Months(self.c_frequency * i) >= val_date ) and
               ( self.matDate - Months(self.c_frequency * i) > self.startDate )):
            day = self.calendar.nextBusinessDay(self.matDate - Months(self.c_frequency * i))
            coup = [day] + coup
            i += 1
        return coup

    def couponDays(self, val_date):
        dates = self.couponPayment(val_date)
        l     = (len(dates) - 1)
        days  = [0] * l
        n = 0
        for i in range(0, l):
            n += dates[i + 1] - dates[i]
            days[i] = n                       #  se deben acumular para el factor de descuento
        return days

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

    def couponDays(self, val_date):
        dates = self.couponPayment(val_date)
        l     = (len(dates) - 1)
        days  = [0] * l
        n = 0
        for i in range(0, l):
            n      += self.calendar.businessDaysBetween(dates[i], dates[i + 1])
            days[i] = n
        return days

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

    val_date = Date(29,12, 2005)
    carter = Portfolio()

    b1 = Bond(nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2030, ),
              base="ACT/ACT", curve_irr="ES_BOND", curve_spread="iBoxx",
              coupon=0.0178246127679505, c_frequency=1, fix_flo=True)

    carter.append(b1)

    b2 = Bond(nominal = 2, startDate = Date(16,10, 2105), matDate = Date(31,10, 2044),
              base="ACT/ACT", curve_irr="ES_BOND", curve_spread="iBoxx",
              coupon=0.0223354303582122, c_frequency=1, fix_flo=True)

    carter.append(b2)

    b3 = BondInf(nominal = 1000, startDate = Date(15, 5, 2005), matDate = Date(15, 5, 2015),
                 base="BUSS/252", curve_irr="BR_BOND", curve_spread="iBoxx", coupon=0,
                 c_frequency=1, fix_flo=True, day=15, IPCA=1.532670225, IPCA_p=1)

    carter.append(b3)

    carter.append(Cash(3))

    # print(carter.NPV(Date(29,12, 2012)))

    c = b1.couponDays(val_date)
    for i in c: print(i)