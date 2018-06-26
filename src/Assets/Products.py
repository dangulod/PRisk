from src.dates.date import Date, Days, Weeks, Months, Quarters, Semesters, Years
from src.dates.conventions import DayCounter, Thirty360, Actual360, Actual365, BUSS252
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
from src.curves.curve import Curve

class Product:
    def __init__(self):
        pass

    def NPV(self, val_date):
        pass


class BondZeroCoupon(Product):
    def __init__(self, nominal, startDate, matDate, curve_irr,
                 curve_spread, base=Actual365(), calendar = Calendar()):
        if not isinstance(base, DayCounter):
            raise ValueError("base must a DayCounter class")
        if not isinstance(calendar, Calendar):
            raise ValueError("calendar must be a calendar class")
        if not isinstance(startDate, Date) or not isinstance(matDate, Date):
            raise ValueError("startDate and matDate must be Date classes")
        if not isinstance(curve_irr, Curve) or not isinstance(curve_spread, Curve):
            raise ValueError("curve_irr and curve_spread must be Curve classes")
        self.nominal = nominal
        self.startDate = startDate
        self.matDate = matDate
        self.base = base
        self.curve_irr = curve_irr
        self.curve_spread = curve_spread
        self.calendar = calendar

    def discount(self, val_date):                   ### ¿¿¿DONDE ESTA VALDATE???? ### No se necesita
        irr    = self.curve_irr.rate(self.matDate)
        spread = self.curve_spread.rate(self.matDate)
        return irr + spread

    def NPV(self, val_date):
        return self.nominal / (( 1 + self.discount(val_date)) ** self.base.yearFraction(val_date, self.matDate ))


class Bond(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 c_frequency, base = Actual365(), calendar = Calendar()):
        super().__init__(nominal, startDate, matDate, curve_irr,
                         curve_spread, base=base, calendar=calendar)
        self.coupon       = coupon
        self.c_frequency  = int(12 / c_frequency)

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
            days[i] = n
        return days

    def NPV(self, val_date):
        dates = self.couponPayment(val_date)
        irr = self.curve_irr.rate(dates)
        spread = self.curve_spread.rate(dates)
        l = len(irr)
        r = [0] * l
        value = 0

        for i in range(0, l):
            r[i] = irr[i] + spread[i]

        for i in range(0, l):
            value += self.coupon / ((1 + r[i]) ** self.base.yearFraction(val_date, dates[i], self.calendar))

        value += self.nominal / ((1 + r[i]) ** self.base.yearFraction(val_date, self.matDate, self.calendar))

        return value


class BondZeroCouponInf(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 c_frequency, day, IPCA, IPCA_p, base=BUSS252(), calendar = Brazil()):
        super().__init__(nominal, startDate, matDate,
                         coupon, c_frequency, curve_irr,
                         curve_spread, base=base, calendar=calendar)
        self.day    = day
        self.IPCA   = IPCA
        self.IPCA_p = IPCA_p

    def NPV(self, val_date):
        return self.nominal


class BondInf(Bond):
    def __init__(self, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 c_frequency, day, IPCA, IPCA_p, base=BUSS252(), calendar=Brazil()):
        super().__init__(nominal, startDate, matDate,
                         curve_irr, curve_spread, coupon,
                         c_frequency, base=base, calendar=calendar)
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

    valDate = Date(29,12, 2015)
    carter = Portfolio()

    days = [valDate + Days(180), valDate + Days(360), valDate + Days(720), valDate + Days(1080),
            valDate + Days(1800), valDate + Days(2520), valDate + Days(3600)]

    rates = [-0.00326, -0.00382, -0.00172, -0.00035,
              0.00401, 0.01029, 0.01908]

    PT_BOND = Curve("PT_BOND", days, rates)

    bc = BondZeroCoupon(nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2020),
                        curve_irr=PT_BOND, base=Actual365(), curve_spread=PT_BOND)

    b1 = Bond(nominal=1, startDate=Date( 3, 4, 2015), matDate=Date(30, 7, 2020),
              curve_irr=PT_BOND, curve_spread=PT_BOND, coupon=0.0178246127679505,
              c_frequency=1, base=Actual365())

    carter.append(b1)

    b2 = Bond(nominal=2, startDate=Date(16,10, 2105), matDate=Date(31,10, 2044),
              base=Actual365(), curve_irr=PT_BOND, curve_spread=PT_BOND,
              coupon=0.0223354303582122, c_frequency=12)

    carter.append(b2)

    b3 = BondInf(nominal=1000, startDate=Date(15, 5, 2005), matDate=Date(15, 5, 2015),
                 base=BUSS252(), curve_irr=PT_BOND, curve_spread=PT_BOND, coupon=0,
                 c_frequency=1, day=15, IPCA=1.532670225, IPCA_p=1)

    carter.append(b3)

    carter.append(Cash(3))

    print(bc.NPV(valDate))
    print(b1.NPV(valDate))

    c = b1.couponPayment(valDate)
    for i in c: print(i)
