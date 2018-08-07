from src.curves.curve import Curve
from src.dates.date import Date, Periods, Days
from math import log, exp, sqrt


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
    '''
    def __init__(self, curve: Curve, MRV, MRS, val_date: Date, t: Periods, flag: bool):
        super().__init__(val_date=val_date, t=t, flag=flag)
        if not isinstance(curve, Curve):
            raise ValueError("Curve is not a Curve class")
        self.curve = curve
        self.MRV   = MRV
        self.MRS   = MRS
        self.dt = self.curve.base.yearFraction(d1=self.val_date, d2=self.val_date + self.t, calendar=self.curve.calendar)

    def sim(self, random):
        l = len(self.curve.rates)
        rates = [0] * l

        dfT = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t)[0]
        dftt = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t + Days(1))[0]
        fm0t = -(log(dftt) - log(dfT)) * 365

        dfT = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t)[0]
        dftt = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t + Days(1))[0]
        fm0s = -(log(dftt) - log(dfT)) * 365

        alfat = fm0t + self.MRV ** 2 / (2 * self.MRS ** 2) * (1 - exp(-self.MRS * self.dt)) ** 2
        alfas = fm0s

        rs = self.curve.rates[0]

        ert = rs * exp(-self.MRS * self.dt) + alfat - alfas * exp(-self.MRS * self.dt)

        vart = self.MRV ** 2 / (2 * self.MRS) * (1 - exp(-2 * self.MRS * self.dt))

        rt = ert + sqrt(vart) * random

        for i in range(0, l):
            dtenor = self.curve.base.yearFraction(d1=self.val_date, d2=self.curve.dates[i], calendar=self.curve.calendar)
            BTT = 1 / self.MRS * (1 - exp(-self.MRS * dtenor))
            dfT = self.curve.discount(val_date=self.val_date, date=self.val_date + self.t)[0]
            dftt = self.curve.discount(val_date=self.val_date, date=self.curve.dates[i] + self.t)[0]
            AtT = dftt / dfT * exp(BTT * fm0t - self.MRV ** 2 / (4 * self.MRS) *
                                   (1 - exp(-2 * self.MRS * self.dt)) * BTT ** 2)
            PtT = AtT * exp(-BTT * rt)
            rates[i] = (1 / PtT) ** (365 / (self.curve.dates[i] - self.val_date)) - 1

        return rates

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
        self.fwd   = self.curve.FWD(val_date, t)

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
    #for i in (iBoxx_m.sim(-0.346714768955995)): print(i)
