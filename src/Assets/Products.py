from src.dates.date import Date, Days, Weeks, Months, Quarters, Semesters, Years
from src.dates.conventions import DayCounter, Thirty360, Actual360, Actual365, BUSS252
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
from src.curves.curve import Curve, IRR, NullCurve


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

    def discount(self, val_date):
        irr    = self.curve_irr.rate(self.matDate)
        spread = self.curve_spread.rate(self.matDate)
        return irr + spread

    def NPV(self, val_date):
        return self.nominal / (( 1 + self.discount(val_date)) ** self.base.yearFraction(val_date,
                                                                                        self.matDate,
                                                                                        self.calendar ))


class Bond(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 frequency, base = Actual365(), calendar = Calendar()):
        super().__init__(nominal, startDate, matDate, curve_irr,
                         curve_spread, base=base, calendar=calendar)
        self.coupon       = coupon
        self.frequency  = int(12 / frequency)

    def couponPayment(self, val_date):
        if (val_date > self.matDate): return 0
        i = 1
        coup = [self.matDate]
        while (( self.matDate - Months(self.frequency * i) >= val_date ) and
               ( self.matDate - Months(self.frequency * i) > self.startDate )):
            day = self.calendar.nextBusinessDay(self.matDate - Months(self.frequency * i))
            coup = [day] + coup
            i += 1
        return coup

    def couponDays(self, val_date):             # Borrar metodo por que no usa calendario y no se usa en NPV
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

        for i in range(0, l): r[i] = irr[i] + spread[i]

        for i in range(0, l):
            value += (self.coupon * self.nominal) / ((1 + r[i]) ** self.base.yearFraction(val_date, dates[i], self.calendar))

        value += self.nominal / ((1 + r[i]) ** self.base.yearFraction(val_date, self.matDate, self.calendar))

        return value


class NTN_B_P(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr,day, IPCA, IPCA_p,
                 curve_spread=NullCurve(), base=BUSS252(), calendar = Brazil()):
        super().__init__(nominal, startDate, matDate, curve_irr,
                         curve_spread=curve_spread, base=base, calendar=calendar)
        self.day    = day
        self.IPCA   = IPCA
        self.IPCA_p = IPCA_p

    def NPV(self, val_date):

        irr    = self.curve_irr.rate(self.matDate)
        spread = self.curve_spread.rate(self.matDate)

        r = irr + spread

        value = 1 / ((1 + r[i]) ** self.base.yearFraction(val_date, self.matDate, self.calendar))

        return self.VNA(val_date) * value


class IndexedNominalBond(Bond):
    def __init__(self, nominal, startDate, matDate, curve_irr, coupon, frequency, index,
                 index_p, day=15, curve_spread=NullCurve(), base=BUSS252(), calendar=Calendar()):
        super().__init__(nominal, startDate, matDate,
                         curve_irr, curve_spread, coupon,
                         frequency, base=base, calendar=calendar)
        self.day     = day
        self.index   = index
        self.index_p = index_p

    def couponDays(self, val_date):
        dates = [val_date] + self.couponPayment(val_date)
        l     = (len(dates) - 1)
        days  = [0] * l
        n     = 0
        for i in range(0, l):
            n      += self.calendar.businessDaysBetween(dates[i], dates[i + 1]) + 1
            days[i] = n
        return days

    def VNA(self, val_date: Date):
        m  = val_date.month()
        y  = val_date.year()
        nd = Date(self.day, m, y)
        pd = nd - Months(1)
        x  = ( val_date - pd ) / ( nd - pd )

        return self.nominal * self.index *( 1 + self.index_p ) ** x

    def NPV(self, val_date):
        dates = self.couponPayment(val_date)

        if dates == 0: return 0

        f = self.frequency / 12

        irr = self.curve_irr.rate(dates)
        spread = self.curve_spread.rate(dates)
        l = len(irr)
        r = [0] * l
        value = 0

        for i in range(0, l): r[i] = irr[i] + spread[i]

        for i in range(0, l):
            value += (((1 + self.coupon) ** ( f ) - 1 ) / (
                        (1 + r[i]) ** self.base.yearFraction(val_date, dates[i], self.calendar)))

        value += 1 / ((1 + r[i]) ** self.base.yearFraction(val_date, self.matDate, self.calendar))

        return self.VNA(val_date) * value


class NTN_B(IndexedNominalBond):
    def __init__(self, nominal, startDate, matDate, curve_irr, coupon, frequency, IPCA,
                 IPCA_p, day=15, curve_spread=NullCurve(), base=BUSS252(), calendar=Brazil()):
        super().__init__(nominal, startDate, matDate, curve_irr, coupon, frequency, index=IPCA,
                         index_p=IPCA_p, day=day, curve_spread=curve_spread, base=base, calendar=calendar)

    def VNA(self, val_date: Date):
        return super().VNA(val_date)

    def NPV(self, val_date):
        return super().NPV(val_date)

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

    valDate = Date(31,12, 2017)
    carter = Portfolio()

    PT_BOND = Curve(name="PT_BOND",
                    dates=[valDate + Days(180), valDate + Days(360), valDate + Days(720),
                           valDate + Days(1080), valDate + Days(1800), valDate + Days(2520),
                           valDate + Days(3600)],
                    rates=[-0.00326, -0.00382, -0.00172, -0.00035, 0.00401, 0.01029, 0.01908])

    ES_BOND = Curve(name="ES_BOND",
                    dates=[valDate + Days(360), valDate + Days(1080), valDate + Days(1440), valDate + Days(1800),
                           valDate + Days(2520), valDate + Days(3240), valDate + Days(3600), valDate + Days(5400),
                           valDate + Days(5580), valDate + Days(7200)],
                    rates=[-0.00528, -0.00024, 0.0006, 0.0037, 0.00819,
                            0.01322, 0.01558, 0.02225, 0.0223, 0.02361])

    iBoxx = Curve(name="iBoxx",
                  dates=[valDate + Days(691), valDate + Days(1397), valDate + Days(2056), valDate + Days(3035),
                         valDate + Days(3222), valDate + Days(4532), valDate + Days(5580), valDate + Days(7223)],
                  rates=[-0.04, 0.002, 0.0051, 0.0088, 0.00932552530590786,
                         0.013, 0.0153331790380074, 0.0174148226736888])

    bc = BondZeroCoupon(nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2020),
                        curve_irr=PT_BOND, curve_spread=PT_BOND, base=Actual365())

    b1 = Bond(nominal=4776736, startDate=Date( 4, 3, 2015), matDate=Date(30, 7, 2030),
              curve_irr=ES_BOND, coupon=0.0178246127679505, curve_spread=NullCurve(),
              frequency=1, base=Actual365())

    b3 = NTN_B(nominal=1000, startDate=Date(15, 5, 2005), matDate=Date(15, 5, 2017),
               base=BUSS252(), curve_irr=IRR(0.0532), coupon=0.06,
               frequency=2, day=15, IPCA=2.097583332, IPCA_p=0.0053)

    print(bc.NPV(valDate))
    print(b1.NPV(valDate))
    print(b3.NPV(Date( 3, 1, 2012)))

    c = b3.couponPayment(Date( 3, 1, 2012))
    for i in c: print(i)
