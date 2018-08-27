from src.dates.date import Date, Days, Months, Years, Periods
from src.dates.calendar import Calendar
from src.dates.calendars.Brazil import Brazil
from src.curves.curve import Curve, IRR, NullCurve
from src.utils.getters import get_base
from src.simulation.factor import Factor


class Product:
    def __init__(self, val_date: Date, t: Periods, **kwargs):
        if not isinstance(t, Periods):
            raise ValueError("t is not a Period class")
        if not isinstance(val_date, Date):
            raise ValueError("t is not a Date class")
        self.val_date = val_date
        self.t = t

    def NPV(self):
        pass

    def __add__(self, other):
        if isinstance(other, Product):
            p = Portfolio()
            p + self
            p + other
            return p


class BondZeroCoupon(Product):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr,
                 curve_spread, base="ACT/365", calendar=Calendar(), **kwargs):
        if not isinstance(calendar, Calendar):
            raise ValueError("calendar must be a calendar class")
        if not isinstance(startDate, Date) or not isinstance(matDate, Date):
            raise ValueError("startDate and matDate must be Date classes")
        if not isinstance(curve_irr, Curve) or not isinstance(curve_spread, Curve):
            raise ValueError("curve_irr and curve_spread must be Curve classes")
        super().__init__(val_date=val_date, t=t, **kwargs)
        self.nominal = nominal
        self.startDate = startDate
        self.matDate = matDate
        self.base = get_base(base)
        self.curve_irr = curve_irr
        self.curve_spread = curve_spread
        self.calendar = calendar

    def val(self, val_date):
        return val_date > self.matDate

    def discount(self):
        irr = self.curve_irr.rate(self.matDate)[0]
        spread = self.curve_spread.rate(self.matDate)[0]
        return irr + spread

    def NPV(self, ):
        if (self.val(self.val_date)): return 0

        curve = self.curve_irr + self.curve_spread
        disc = curve.discount(val_date=self.val_date, date=self.matDate)[0]
        return self.nominal * disc


class Bond(BondZeroCoupon):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 frequency, base="ACT/365", calendar=Calendar(), **kwargs):
        super().__init__(val_date=val_date, t=t, nominal=nominal, startDate=startDate, matDate=matDate,
                         curve_irr=curve_irr, curve_spread=curve_spread, base=base, calendar=calendar, **kwargs)
        if (not isinstance(frequency, int) or frequency < 1):
            raise ValueError("frequency must be an integer greater than 0. Consider the BondZeroCoupon pricer")
        self.coupon = coupon
        self.frequency = int(12 / frequency)
        self.c_dates = self.couponPayment()[1:]
        self.first = self.couponPayment()[0]

    def couponPayment(self):
        if (self.val_date > self.matDate): return 0
        i = 1
        coup = [self.matDate]
        while ((self.matDate - Months(self.frequency * i) >= self.val_date) and
               (self.matDate - Months(self.frequency * i) > self.startDate)):
            day = self.matDate - Months(self.frequency * i)
            # day = self.calendar.nextBusinessDay(self.matDate - Months(self.frequency * i))
            coup = [day] + coup
            i += 1
        first = self.matDate - Months(self.frequency * i)
        coup = [first] + coup
        return coup

    def NPV(self):
        if (self.val(self.val_date)): return 0

        curve = self.curve_irr + self.curve_spread
        disc = curve.discount(val_date=self.val_date, date=self.c_dates)

        l = len(self.c_dates)

        value = 0

        for i in range(0, l):
            if not i == 0:
                c = self.coupon * self.base.yearFraction(self.c_dates[i - 1], self.c_dates[i], calendar=self.calendar)
            else:
                c = self.coupon * self.base.yearFraction(self.first, self.c_dates[i], calendar=self.calendar)

            value += c * disc[i]  # Este debería ser el calendar de la curva, no del producto

        value += 1 * disc[l - 1]

        return value * self.nominal


class BondFloating(Bond):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr, curve_spread, coupon,
                 frequency, base="ACT/365", calendar=Calendar(), **kwargs):
        super().__init__(val_date=val_date, t=t, nominal=nominal, startDate=startDate, matDate=matDate,
                         curve_irr=curve_irr, curve_spread=curve_spread, base=base, calendar=calendar,
                         coupon=coupon, frequency=frequency, **kwargs)

    def NPV(self):
        if (self.val(self.val_date)): return 0

        curve = self.curve_irr + self.curve_spread

        l = len(self.c_dates)

        cf = [0] * l
        cf[0] = curve.rate(self.val_date + Months(self.frequency))[0] * self.frequency / 12

        d = curve.discount(self.val_date, self.c_dates)
        value = cf[0] * d[0]
        for i in range(1, l):
            cf[i] = curve.simple_forward(val_date=self.val_date, t1=self.c_dates[i - 1],
                                         t2=self.c_dates[i]) * self.frequency / 12
            value += cf[i] * d[i]

        value += 1 * d[l - 1]

        return value * self.nominal


class NTN_B_P(BondZeroCoupon):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr, IPCA, IPCA_p: Curve, day=15,
                 curve_spread=NullCurve(), base="BUSS/252", calendar=Brazil(), **kwargs):
        super().__init__(val_date=val_date, t=t, nominal=nominal, startDate=startDate, matDate=matDate,
                         curve_irr=curve_irr, curve_spread=curve_spread, base=base, calendar=calendar, **kwargs)
        self.day = day
        self.IPCA = IPCA
        self.curve_index = IPCA_p

    def VNA(self):
        m = self.val_date.month()
        y = self.val_date.year()
        nd = Date(self.day, m, y)
        pd = nd - Months(1)
        x = (self.val_date - pd) / (nd - pd)
        p = self.curve_index.rate(self.val_date + t)[0]

        return self.nominal * self.IPCA * (1 + p) ** x

    def NPV(self):
        if (self.val(self.val_date)): return 0

        irr = self.curve_irr.rate(self.matDate)
        spread = self.curve_spread.rate(self.matDate)

        r = irr[0] + spread[0]

        value = 1 / ((1 + r) ** (self.base.yearFraction(self.val_date, self.matDate, self.calendar)))

        return self.VNA() * value


class IndexedNominalBond(Bond):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr, coupon, frequency, index,
                 curve_index: Curve, day=15, curve_spread=NullCurve(), base="BUSS/252", calendar=Calendar(), **kwargs):
        super().__init__(val_date=val_date, t=t, nominal=nominal, startDate=startDate, matDate=matDate,
                         curve_irr=curve_irr, curve_spread=curve_spread, coupon=coupon, frequency=frequency,
                         base=base, calendar=calendar, **kwargs)
        self.day = day
        self.index = index
        self.curve_index = curve_index

    '''
    def couponDays(self, val_date):
        dates = [val_date] + self.couponPayment(val_date)
        l     = (len(dates) - 1)
        days  = [0] * l
        n     = 0
        for i in range(0, l):
            n      += self.calendar.businessDaysBetween(dates[i], dates[i + 1])
            days[i] = n
        return days
    '''

    def VNA(self):
        m = self.val_date.month()
        y = self.val_date.year()
        nd = Date(self.day, m, y)
        pd = nd - Months(1)
        # x  = ( val_date - pd ) / ( nd - pd )
        x = (self.val_date + self.t - pd) / (nd + t - pd)

        p = self.curve_index.rate(self.val_date + self.t)[0]

        return self.nominal * self.index * (1 + p) ** x

    def NPV(self):
        if (self.val(self.val_date)): return 0

        f = self.frequency / 12

        l = len(self.c_dates)

        value = 0

        curve = self.curve_irr + self.curve_spread
        r = curve.rate(self.c_dates)

        for i in range(0, l):
            value += (((1 + self.coupon) ** (f) - 1) / (
                    (1 + r[i]) ** self.base.yearFraction(self.val_date, self.c_dates[i], self.calendar)))

        value += 1 / ((1 + r[l - 1]) ** self.base.yearFraction(self.val_date, self.matDate, self.calendar))

        return self.VNA() * value


class NTN_B(IndexedNominalBond):
    def __init__(self, val_date: Date, t: Periods, nominal, startDate, matDate, curve_irr, coupon, frequency, IPCA,
                 IPCA_p, day=15, curve_spread=NullCurve(), base="BUSS/252", calendar=Brazil(), **kwargs):
        super().__init__(val_date=val_date, t=t, nominal=nominal, startDate=startDate, matDate=matDate,
                         curve_irr=curve_irr,
                         coupon=coupon, frequency=frequency, index=IPCA, curve_index=IPCA_p, day=day,
                         curve_spread=curve_spread, base=base, calendar=calendar, **kwargs)

    def VNA(self):
        return super().VNA()

    def NPV(self):
        if (self.val(self.val_date)): return 0
        return super().NPV()


class Equity(Product):
    def __init__(self, val_date: Date, t: Periods, nominal, factor: Factor, **kwargs):
        super().__init__(val_date=val_date, t=t)
        self.nominal = nominal
        self.factor = factor

    def NPV(self):
        return self.nominal * self.factor.getFactor()


class Cash(Product):
    def __init__(self, val_date: Date, t: Periods, nominal, **kwargs):
        super().__init__(val_date=val_date, t=t)
        self.nominal = nominal

    def NPV(self):
        return self.nominal


class Portfolio:
    def __init__(self):
        self.products = []

    def append(self, p):
        if (not isinstance(p, Product)):
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
    def create_portfolio(list: list):
        x = Portfolio()
        for i in list:
            x + i
        return x

    def NPV(self):
        if self.__len__() == 0:
            return 0

        value = 0
        for i in self.products:
            value += i.NPV()

        return value


if __name__ == "__main__":

    val_date = Date(31, 12, 2017)
    t = Years(1)
    carter = Portfolio()

    IT_BOND = Curve(name="IT_BOND",
                    dates=[Date(31, 5, 2018) + Days(90), Date(31, 5, 2018) + Days(180), Date(31, 5, 2018) + Days(360),
                           Date(31, 5, 2018) + Days(720), Date(31, 5, 2018) + Days(1080),
                           Date(31, 5, 2018) + Days(2160),
                           Date(31, 5, 2018) + Days(2520), Date(31, 5, 2018) + Days(2880),
                           Date(31, 5, 2018) + Days(3600),
                           Date(31, 5, 2018) + Days(5400), Date(31, 5, 2018) + Days(5580)],
                    rates=[-0.00223, 0.00205, 0.00515, 0.00991, 0.01342, 0.02326,
                           0.02385, 0.02560, 0.02771, 0.03047, 0.03047])

    PT_BOND = Curve(name="PT_BOND",
                    dates=[val_date + Days(180), val_date + Days(360), val_date + Days(720),
                           val_date + Days(1080), val_date + Days(1800), val_date + Days(2520),
                           val_date + Days(3600)],
                    rates=[-0.00326, -0.00382, -0.00172, -0.00035, 0.00401, 0.01029, 0.01908])

    ES_BOND = Curve(name="ES_BOND",
                    dates=[val_date + Days(360), val_date + Days(1080), val_date + Days(1440), val_date + Days(1800),
                           val_date + Days(2520), val_date + Days(3240), val_date + Days(3600), val_date + Days(5400),
                           val_date + Days(5580), val_date + Days(7200)],
                    rates=[-0.00528, -0.00024, 0.0006, 0.0037, 0.00819,
                           0.01322, 0.01558, 0.02225, 0.0223, 0.02361])

    iBoxx = Curve(name="iBoxx",
                  dates=[val_date + Days(691), val_date + Days(1397), val_date + Days(2056), val_date + Days(3035),
                         val_date + Days(3222), val_date + Days(4532), val_date + Days(5580), val_date + Days(7223)],
                  rates=[-0.04, 0.002, 0.0051, 0.0088, 0.00932552530590786,
                         0.013, 0.0153331790380074, 0.0174148226736888])

    IR_iBoxx = Curve(name="IR_iBoxx",
                     dates=[val_date + Days(659), val_date + Days(1429), val_date + Days(1850), val_date + Days(2801),
                            val_date + Days(4399), val_date + Days(7210), val_date + Days(8406)],
                     rates=[0.0098, 0.0126, 0.0146, 0.0176, 0.021600, 0.023564, 0.0244])

    IPCA = Curve(name="IPCA",
                 dates=[val_date + Days(360), val_date + Days(720), val_date + Days(1080), val_date + Days(1440),
                        val_date + Days(1800), val_date + Days(2160), val_date + Days(2520), val_date + Days(2880),
                        val_date + Days(3240), val_date + Days(3600), val_date + Days(4320), val_date + Days(5400),
                        val_date + Days(5580), val_date + Days(7200), val_date + Days(9000), val_date + Days(10800)],
                 rates=[0.014096, 0.013621, 0.013896, 0.014096, 0.014496, 0.014796, 0.015046, 0.015346,
                        0.015696, 0.016021, 0.016704, 0.017591, 0.017705, 0.018735, 0.019405, 0.019725])

    bc = BondZeroCoupon(val_date=val_date, t=t, nominal=1, startDate=Date(3, 4, 2015), matDate=Date(30, 7, 2020),
                        curve_irr=PT_BOND, curve_spread=PT_BOND, base="ACT/365")

    b1 = Bond(val_date=val_date, t=t, nominal=4776736, startDate=Date(4, 3, 2015), matDate=Date(30, 7, 2030),
              curve_irr=ES_BOND, coupon=0.0178246127679505, curve_spread=NullCurve(),
              frequency=1, base="ACT/365")

    bu = Bond(val_date=val_date, t=t, nominal=1952048, startDate=Date(15, 1, 2014), matDate=Date(15, 9, 2076),
              curve_irr=IR_iBoxx, coupon=0.0206653578940817, curve_spread=NullCurve(),
              frequency=3, base="ACT/365")

    b3 = NTN_B(val_date=val_date, t=t, nominal=1000, startDate=Date(15, 5, 2005), matDate=Date(15, 5, 2017),
               base="BUSS/252", curve_irr=IRR(0.0532), coupon=0.06, calendar=Brazil(),
               frequency=2, day=15, IPCA=2.097583332, IPCA_p=IRR(0.0053))

    b4 = NTN_B_P(val_date=val_date, t=t, nominal=1000, startDate=Date(15, 7, 2000), matDate=Date(15, 5, 2015),
                 curve_irr=IRR(0.0874), IPCA=1.532670225, IPCA_p=IRR(0))

    b5 = NTN_B(val_date=val_date, t=t, nominal=1000, startDate=Date(8, 9, 2004), matDate=Date(1, 4, 2008),
               curve_irr=IRR(0.0853), coupon=6, frequency=2, IPCA=1.754670875, IPCA_p=IRR(1), day=1)

    b6 = NTN_B(val_date=val_date, t=t, nominal=160, startDate=Date(15, 5, 2015), matDate=Date(15, 5, 2023),
               curve_irr=IRR(0.048892272), IPCA=1, IPCA_p=IRR(0.029734), coupon=0.06, frequency=2)

    b7 = BondFloating(val_date=val_date, t=t, nominal=10064000, startDate=Date(8, 11, 2007), matDate=Date(23, 12, 2044),
                      curve_irr=iBoxx, curve_spread=NullCurve(), coupon=0, base="30/360", frequency=1)

    b8 = BondFloating(val_date=Date(31, 5, 2018), t=Years(1), nominal=4929515, startDate=Date(3, 5, 2015),
                      matDate=Date(3, 5, 2025), curve_irr=IT_BOND, curve_spread=NullCurve(), coupon=0,
                      base="30/360", frequency=4)

    print(bc.NPV())
    print(b1.NPV())
    print(bu.NPV())
    print(b3.NPV())

    print(b4.NPV())
    print(b5.NPV())
    print(b6.NPV())
    print(b7.NPV())
    print(b8.NPV())

    for i in b1.couponPayment(): print(i)

