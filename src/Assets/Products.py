class Product:
    def __init__(self):
        pass

    def NPV(self, val_date):
        pass

class Bond(Product):
    def __init__(self, nominal, startDate, matDate, base, curve_irr, curve_spread, coupon, c_frequency, fix_flo, calendar = Brasil()):
        self.nominal      = nominal
        self.startDate    = startDate
        self.matDate      = matDate
        self.base         = base
        self.curve_irr    = curve_irr
        self.curve_spread = curve_spread
        self.coupon       = coupon,
        self.c_frequency  = c_frequency
        self.fix_flo      = fix_flo

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
    def __init__(self, products : Product):
        self.products = products

    def NPV(self, val_date):
        value = 0
        for i in self.products:
            value += i.NPV(val_date)
        return value

if __name__ == "__main__":
    from datetime import date

    x1 = Bond(nominal     = 1, # 4776736,
             startDate    = date(2015, 3, 4),
             matDate      = date(2030, 7, 30),
             base         = "ACT/ACT",
             curve_irr    = "ES_BOND",
             curve_spread = "iBoxx",
             coupon       = 0.0178246127679505,
             c_frequency  = 1,
             fix_flo      = True)

    x2 = Bond(nominal     = 2, # 5837512,
             startDate    = date(2015,10,16),
             matDate      = date(2044,10,31),
             base         = "ACT/ACT",
             curve_irr    = "ES_BOND",
             curve_spread = "iBoxx",
             coupon       = 0.0223354303582122,
             c_frequency  = 1,
             fix_flo      = True)

    c = Cash(3)
    x = Portfolio([x1, x2, c])

    print(x.NPV(1))