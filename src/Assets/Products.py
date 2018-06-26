from src.dates.date import Date, Days, Weeks, Months, Quarters, Semesters, Years
from src.dates.conventions import DayCounter, Thirty360, Actual360, Actual365, BUSS252
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
from src.curves import curve

class Product:
    def __init__(self):
        pass

    def NPV(self, val_date):
        pass


class BondZeroCoupon(Product):
    def __init__(self, nominal, startDate, matDate, base, curve_irr,
                 curve_spread, calendar = Calendar()):
        #if not isinstance(base, DayCounter):
        #    raise ValueError("base must a DayCounter class")
        if not isinstance(calendar, Calendar):
            raise ValueError("calendar must be a calendar class")
        if not isinstance(startDate, Date) or not isinstance(matDate, Date):
            raise ValueError("startDate and matDate must be Date classes")
        # if not isinstance(curve_irr, curve) and not isinstance(curve_spread, curve):
        #    raise ValueError("curve_irr and curve_spread must be Date")
        self.nominal = nominal
        self.startDate = startDate
        self.matDate = matDate
        self.base = base
        self.curve_irr = curve_irr
        self.curve_spread = curve_spread
        self.calendar = calendar

    def NPV(self, val_date):
        irr = self.curve_irr.discount(val_date, self.mat_date, self.base)

        return self.nominal * irr


class Bond(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, calendar = Calendar()):
        super().__init__(nominal, startDate, matDate, base,
                         curve_irr, curve_spread, calendar)
        self.coupon       = coupon,
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
        amor   = super().NPV()                              # NPV del principal
        pagos  = self.couponDates(val_date)                 # Array de fechas de cupones

        irr    = self.curve_irr.rate(pagos)                 # Risk free a cada fecha
        spread = self.curve_spread.rate(pagos)              # Spread a cada fecha

        disc   = irr + spread                               # Array de tasa de descuento

        disc_f  = 1 / (( 1 + disc) ** self.base.yearFraction(val_date, pagos, self.calendar ))    # Array factor de descuento
        disc_f * self.coupon

        sum(disc_f) * self.coupon

        valor   = amor + disc_f
        return valor


class BondZeroCouponInf(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, day, IPCA, IPCA_p, calendar = Brazil()):
        super().__init__(nominal, startDate, matDate, base,
                         coupon, c_frequency, curve_irr,
                         curve_spread, calendar = calendar)
        self.day    = day
        self.IPCA   = IPCA
        self.IPCA_p = IPCA_p

    def NPV(self, val_date):
        return self.nominal


class BondInf(Bond):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon,
                 c_frequency, day, IPCA, IPCA_p, calendar = Brazil()):
        super().__init__(nominal, startDate, matDate, base,
                         curve_irr, curve_spread, coupon,
                         c_frequency, calendar = calendar)
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

    val_date = Date(29,12, 2015)
    carter = Portfolio()

    b1 = Bond(nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2020),
              base="ACT/ACT", curve_irr="ES_BOND", curve_spread="iBoxx",
              coupon=0.0178246127679505, c_frequency=1)

    carter.append(b1)

    b2 = Bond(nominal = 2, startDate = Date(16,10, 2105), matDate = Date(31,10, 2044),
              base="ACT/ACT", curve_irr="ES_BOND", curve_spread="iBoxx",
              coupon=0.0223354303582122, c_frequency=12)

    carter.append(b2)

    b3 = BondInf(nominal = 1000, startDate = Date(15, 5, 2005), matDate = Date(15, 5, 2015),
                 base="BUSS/252", curve_irr="BR_BOND", curve_spread="iBoxx", coupon=0,
                 c_frequency=1, day=15, IPCA=1.532670225, IPCA_p=1)

    carter.append(b3)

    carter.append(Cash(3))

    # print(carter.NPV(Date(29,12, 2012)))

    c = b1.couponPayment(val_date)
    for i in c: print(i)