from src.dates.date import Date, Days, Months
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
from src.curves.curve import Curve, IRR, NullCurve
from src.utils.getters import get_base


class Product:
    def __init__(self, **kwargs):
        pass

    def NPV(self, val_date):
        pass

    def __add__(self, other):
        if isinstance(other, Product):
            p = Portfolio()
            p + self
            p + other
            return p


class BondZeroCoupon(Product):
    def __init__(self, nominal, startDate, matDate, curve_irr,
                 curve_spread, base="ACT/365", calendar=Calendar(), **kwargs):
        if not isinstance(calendar, Calendar):
            raise ValueError("calendar must be a calendar class")
        if not isinstance(startDate, Date) or not isinstance(matDate, Date):
            raise ValueError("startDate and matDate must be Date classes")
        if not isinstance(curve_irr, Curve) or not isinstance(curve_spread, Curve):
            raise ValueError("curve_irr and curve_spread must be Curve classes")
        super().__init__(**kwargs)
        self.nominal = nominal
        self.startDate = startDate
        self.matDate = matDate
        self.base = get_base(base)
        self.curve_irr = curve_irr
        self.curve_spread = curve_spread
        self.calendar = calendar

    def val(self, val_date):
        return val_date > self.matDate

    def discount(self, val_date):
        irr    = self.curve_irr.rate(self.matDate)[0]
        spread = self.curve_spread.rate(self.matDate)[0]
        return irr + spread

    def NPV(self, val_date):
        if (self.val(val_date)): return 0
        return self.nominal / (( 1 + self.discount(val_date)) ** self.base.yearFraction(val_date,
                                                                                        self.matDate,
                                                                                        self.calendar ))


class Bond(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 frequency, base="ACT/365", calendar=Calendar(), **kwargs):
        super().__init__(nominal, startDate, matDate, curve_irr,
                         curve_spread, base=base, calendar=calendar, **kwargs)
        if ( not isinstance(frequency, int) or frequency < 1 ):
            raise ValueError("frequency must be an integer greater than 0. Consider the BondZeroCoupon pricer")
        self.coupon     = coupon
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

    def NPV(self, val_date):
        if (self.val(val_date)): return 0

        f = self.frequency / 12
        c = ((1 + self.coupon) ** (f) - 1)

        dates = self.couponPayment(val_date)
        irr = self.curve_irr.rate(dates)
        spread = self.curve_spread.rate(dates)
        l = len(irr)
        r = [0] * l
        value = 0

        for i in range(0, l): r[i] = irr[i] + spread[i]

        for i in range(0, l):
            value += (c * self.nominal) / ((1 + r[i]) ** self.base.yearFraction(val_date, dates[i], self.calendar))

        value += self.nominal / ((1 + r[i]) ** self.base.yearFraction(val_date, self.matDate, self.calendar))

        return value


class NTN_B_P(BondZeroCoupon):
    def __init__(self, nominal, startDate, matDate, curve_irr, IPCA, IPCA_p, day=15,
                 curve_spread=NullCurve(), base="BUSS/252", calendar=Brazil(), **kwargs):
        super().__init__(nominal, startDate, matDate, curve_irr,
                         curve_spread=curve_spread, base=base, calendar=calendar, **kwargs)
        self.day    = day
        self.IPCA   = IPCA
        self.IPCA_p = IPCA_p

    def VNA(self, val_date: Date):
        m  = val_date.month()
        y  = val_date.year()
        nd = Date(self.day, m, y)
        pd = nd - Months(1)
        x  = ( val_date - pd ) / ( nd - pd )

        return self.nominal * self.IPCA *( 1 + self.IPCA_p ) ** x

    def NPV(self, val_date):
        if (self.val(val_date)): return 0

        irr    = self.curve_irr.rate(self.matDate)
        spread = self.curve_spread.rate(self.matDate)

        r = irr[0] + spread[0]

        value = 1 / ((1 + r) ** ( self.base.yearFraction(val_date, self.matDate, self.calendar)  ))

        return self.VNA(val_date) * value


class IndexedNominalBond(Bond):
    def __init__(self, nominal, startDate, matDate, curve_irr, coupon, frequency, index,
                 index_p, day=15, curve_spread=NullCurve(), base="BUSS/252", calendar=Calendar(), **kwargs):
        super().__init__(nominal, startDate, matDate,
                         curve_irr, curve_spread, coupon,
                         frequency, base=base, calendar=calendar, **kwargs)
        self.day     = day
        self.index   = index
        self.index_p = index_p

    def couponDays(self, val_date):
        dates = [val_date] + self.couponPayment(val_date)
        l     = (len(dates) - 1)
        days  = [0] * l
        n     = 0
        for i in range(0, l):
            n      += self.calendar.businessDaysBetween(dates[i], dates[i + 1])
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
        if (self.val(val_date)): return 0
        dates = self.couponPayment(val_date)

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
                 IPCA_p, day=15, curve_spread=NullCurve(), base="BUSS/252", calendar=Brazil(), **kwargs):
        super().__init__(nominal, startDate, matDate, curve_irr, coupon, frequency, index=IPCA,
                         index_p=IPCA_p, day=day, curve_spread=curve_spread, base=base, calendar=calendar, **kwargs)

    def VNA(self, val_date: Date):
        return super().VNA(val_date)

    def NPV(self, val_date):
        if (self.val(val_date)): return 0
        return super().NPV(val_date)


class Equity(Product):
    def __init__(self, nominal, factor, **kwargs):
        self.nominal = nominal
        self.factor = factor

    def NPV(self, val_date):
        return self.nominal * self.factor


class Cash(Product):
    def __init__(self, value, **kwargs):
        self.value = value

    def NPV(self, val_date):
        return self.value


class Portfolio:
    def __init__(self):
        self.products = []

    def append(self, p):
        if ( not isinstance(p, Product) ):
            raise ValueError("p must be a Product")
        self.products.append(p)

    def __add__(self, other):
        self.append(other)

    def __getitem__(self, item):
        return self.products[item]

    def __len__(self):
        return len(self.products)

    def __str__(self):
        return "PORTFOLIO with " + str(len(self)) + " products"

    def __repr__(self):
        return "PORTFOLIO with " + str(len(self)) + " products"

    @staticmethod
    def create_portfolio(list):
        x = Portfolio()
        for i in list:
            x + i
        return x

    def NPV(self, val_date):
        if self.__len__() == 0:
            return 0

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

    IR_iBoxx = Curve(name="IR_iBoxx",
                     dates=[valDate + Days(659), valDate + Days(1429), valDate + Days(1850), valDate + Days(2801),
                            valDate + Days(4399), valDate + Days(7210), valDate + Days(8406)],
                     rates=[0.0098, 0.0126, 0.0146, 0.0176, 0.021600, 0.023564, 0.0244])

    bc = BondZeroCoupon(nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2020),
                        curve_irr=PT_BOND, curve_spread=PT_BOND, base="ACT/365")

    b1 = Bond(nominal=4776736, startDate=Date( 4, 3, 2015), matDate=Date(30, 7, 2030),
              curve_irr=ES_BOND, coupon=0.0178246127679505, curve_spread=NullCurve(),
              frequency=1, base="ACT/365")

    bu = Bond(nominal=1952048, startDate=Date(15, 1, 2014), matDate=Date(15, 9, 2076),
              curve_irr=IR_iBoxx, coupon=0.0206653578940817, curve_spread=NullCurve(),
              frequency=3, base="ACT/365")

    b3 = NTN_B(nominal=1000, startDate=Date(15, 5, 2005), matDate=Date(15, 5, 2017),
               base="BUSS/252", curve_irr=IRR(0.0532), coupon=0.06,
               frequency=2, day=15, IPCA=2.097583332, IPCA_p=0.0053)

    b4 = NTN_B_P(nominal=1000, startDate=Date(15, 7, 2000), matDate=Date(15, 5, 2015), curve_irr=IRR(0.0874),
                 IPCA=1.532670225, IPCA_p=0)

    '''
    print(bc.NPV(valDate))
    print(b1.NPV(valDate))
    print(b3.NPV(Date( 3, 1, 2012)))
    print(b4.NPV(Date(15, 7, 2005)))
    '''
    print(b1.NPV(valDate))

    '''
    c = b1.couponPayment(Date(31, 12, 2017))
    for i in c: print(i)
    '''
