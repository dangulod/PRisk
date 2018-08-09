from src.curves.curve import Curve
from src.dates.date import Date, Periods, Days
from math import log, exp, sqrt
from src.simulation.factor import Factor

class Model:
    def __init__(self, val_date: Date, t: Periods, flag: bool):
        if not isinstance(flag, bool):
            raise ValueError("flag is not boolean")
        if not isinstance(t, Periods):
            raise ValueError("t is not a Period class")
        if not isinstance(val_date, Date):
            raise ValueError("t is not a Date class")
        self.val_date = val_date
        self.t        = t
        self.flag     = flag


class HullWhite(Model):
    '''
    MRV: Mean Reversion Volatility (sigma)
    MRS: Mean Reversion Speed (alpha)

    Excel implementation

    dftt = DiscountFactorFromCurve(c2, t + inct * 365)
    fm0t = -(Log(dftt) - Log(dfT)) * 365
    dfT = DiscountFactorFromCurve(c2, t - dt * 365)
    dftt = DiscountFactorFromCurve(c2, t - dt * 365 + inct * 365)
    fm0s = -(Log(dftt) - Log(dfT)) * 365
    alfat = fm0t + MRV ^ 2 / (2 * MRS ^ 2) * (1 - Exp(-MRS * t / 365)) ^ 2
    alfas = fm0s + MRV ^ 2 / (2 * MRS ^ 2) * (1 - Exp(-MRS * (t / 365 - dt))) ^ 2
    rs = c.SRate(1)
    Ert = rs * Exp(-MRS * dt) + alfat - alfas * Exp(-MRS * dt)
    Vart = MRV ^ 2 / (2 * MRS) * (1 - Exp(-2 * MRS * dt))
    rt = Ert + Sqr(Vart) * Z
    '''

    def __init__(self, curve: Curve, MRV, MRS, val_date: Date, t: Periods, flag: bool):
        super().__init__(val_date=val_date, t=t, flag=flag)
        if not isinstance(curve, Curve):
            raise ValueError("Curve is not a Curve class")
        self.curve = curve
        self.MRV   = MRV
        self.MRS   = MRS
        self.dt = self.curve.base.yearFraction(d1=self.val_date, d2=self.val_date + self.t, calendar=self.curve.calendar)

        dfT = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t)[0]
        dftt = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t + Days(1))[0]
        self.fm0t = -(log(dftt) - log(dfT)) * 365

        dfT = self.curve.discount(val_date=self.val_date, date=self.val_date )[0]
        dftt = self.curve.discount(val_date=self.val_date, date=self.val_date + Days(1))[0]
        fm0s = -(log(dftt) - log(dfT)) * 365

        alfat = self.fm0t + self.MRV ** 2 / (2 * self.MRS ** 2) * (1 - exp(-self.MRS * self.dt)) ** 2
        alfas = fm0s

        rs = self.curve.rates[0]

        self.ert = rs * exp(-self.MRS * self.dt) + alfat - alfas * exp(-self.MRS * self.dt)
        self.vart = self.MRV ** 2 / (2 * self.MRS) * (1 - exp(-2 * self.MRS * self.dt))

    def sim(self, random):
        rt = self.ert + sqrt(self.vart) * random

        l = len(self.curve.rates)
        rates = [0] * l

        for i in range(0, l):
            dtenor = self.curve.base.yearFraction(d1=self.val_date, d2=self.curve.dates[i], calendar=self.curve.calendar)
            BTT = 1 / self.MRS * (1 - exp(-self.MRS * dtenor))
            dfT = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t)[0]
            dftt = self.curve.discount(val_date=self.val_date, date=self.curve.dates[i] + self.t)[0]
            AtT = dftt / dfT * exp(BTT * self.fm0t - self.MRV ** 2 / (4 * self.MRS) *
                                   (1 - exp(-2 * self.MRS * self.dt)) * BTT ** 2)
            PtT = AtT * exp(-BTT * rt)
            rates[i] = (1 / PtT) ** (365 / (self.curve.dates[i] - self.val_date)) - 1

        return rates

    def var(self, random):
        l = len(self.curve)
        d = [0] * l
        h = self.sim(random=random)

        for i in range(0, l):
            d[i] = h[i] - self.curve.rates[i]

        return d


class LN(Model):
    def __init__(self, factor: Factor, curve: Curve, vol, val_date: Date, t: Periods, flag: bool):
        super().__init__(val_date=val_date, t=t, flag=flag)
        '''
        Excel implementation

        dfF_0 = 1
        If Not IsMissing(CurvaF) And Not IsEmpty(CurvaF) Then
            dfF_0 = DiscountFactor(Range(CurvaF), t - dt * 365)
        End If

        dfF_1 = 1
        If Not IsMissing(CurvaF) And Not IsEmpty(CurvaF) Then
            dfF_1 = DiscountFactor(Range(CurvaF), t)
        End If

        dFWD = DiscountFactor(CurvaL, t - dt * 365) / DiscountFactor(CurvaL, t) * dfF_1 / dfF_0
        MasterSimula = Simula("LNFwd", S, dFWD, MRVaux, 0, 0, 0, dt, Z)
        '''
        if not isinstance(curve, Curve):
            raise ValueError("Curve is not a Curve class")
        self.curve  = curve
        self.factor = factor
        self.vol    = vol
        self.dt     = self.curve.base.yearFraction(d1=self.val_date, d2=self.val_date + t, calendar=self.curve.calendar)
        self.dFWD   = 1 / self.curve.discount(self.val_date, self.val_date + self.t)[0]

    def sim(self, random):
        return self.factor.factor[0] * self.dFWD * exp(-0.5 * self.vol ** 2 * self.dt + self.vol * sqrt(self.dt) * random)


class LnFwd(Model):
    '''

    '''
    def __init__(self, curve: Curve, vol, val_date: Date, t: Periods, flag: bool):
        super().__init__(val_date=val_date, t=t, flag=flag)
        if not isinstance(curve, Curve):
            raise ValueError("Curve is not a Curve class")
        self.curve = curve
        self.vol   = vol
        self.dt    = self.curve.base.yearFraction(d1=self.val_date, d2=self.val_date + t, calendar=self.curve.calendar)
        self.fwd   = self.curve.FWD(self.val_date, self.t)

    def sim(self, random):
        l = len(self.curve)
        rates = [0] * l

        for i in range(0, l):
            rates[i] = self.fwd[i] * exp(-0.5 * self.vol ** 2 * self.dt + self.vol * sqrt(self.dt) * random)

        return rates


if __name__ == "__main__":

    from src.dates.date import Days, Months, Years

    valDate = Date(31,12,2017)

    IPCA = Curve(name="IPCA",
                 dates=[valDate + Days(365), valDate + Days(720), valDate + Days(1080), valDate + Days(1440),
                        valDate + Days(1800), valDate + Days(2160), valDate + Days(2520), valDate + Days(2880),
                        valDate + Days(3240), valDate + Days(3600), valDate + Days(4320), valDate + Days(5400),
                        valDate + Days(5580), valDate + Days(7200), valDate + Days(9000), valDate + Days(10800)],
                 rates=[0.014095800, 0.013620800, 0.013895800, 0.014095800, 0.014495800, 0.014795800,0.015045800,
                        0.015345800, 0.015695800, 0.016020800, 0.016703720, 0.017590600, 0.017704851, 0.018735400,
                        0.019405200, 0.019725000])

    IPCA_m = HullWhite(curve=IPCA, MRV=0.0025, MRS=0.01, val_date=valDate, t=Days(363), flag=True)
    for i in IPCA_m.sim(random=0.167728385139152): print(i)

    iBoxx = Curve(name="iBoxx",
                  dates=[valDate + Days(691), valDate + Days(1397), valDate + Days(2056), valDate + Days(3035),
                        valDate + Days(3222), valDate + Days(4532), valDate + Days(5580), valDate + Days(7223)],
                  rates=[-0.0004000000000000000, 0.0020000000000000000, 0.0051000000000000000, 0.0088000000000000000,
                        0.0093255253059078600, 0.0130000000000000000, 0.0153331790380074000, 0.0174148226736888000])

    iBoxx_m = LnFwd(curve=iBoxx, vol=0.080276396187267, val_date=valDate, t=Days(363), flag=True)

    PT_BOND = Curve(name="PT_BOND",
                    dates=[valDate + Days(180), valDate + Days(360), valDate + Days(720),valDate + Days(1080),
                            valDate + Days(1800), valDate + Days(2520), valDate + Days(3600)],
                    rates=[-0.0278, -0.00233, -0.00068, 0.00167, 0.00778, 0.01381, 0.1956])

    EQ1 = Factor(name="EQ1")

    EQ1 = LN(factor=EQ1, curve=PT_BOND, vol=0.0240619356008235, val_date=valDate, t=Days(363), flag=True)
    
    print(EQ1.sim(2.76929645563361) - 1.06594069317654)


