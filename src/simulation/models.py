from src.curves.curve import Curve
from src.dates.date import Date, Periods, Days
from math import log, exp, sqrt


class Model:
    def __init__(self):
        pass


class HullWhite(Model):
    def __init__(self, curve: Curve, MRV, MRS, flag: bool):
        super().__init__()
        if not isinstance(curve, Curve):
            raise ValueError("Curve is not a Curve class")
        if not isinstance(flag, bool):
            raise ValueError("flag is not boolean")
        self.curve = curve
        self.MRV = MRV
        self.MRS = MRS
        self.flag = flag

    def sim(self, val_date, t, random):
        if not isinstance(t, Periods):
            raise ValueError("t is not a Period class")
        if not isinstance(val_date, Date):
            raise ValueError("t is not a Date class")

        l = len(self.curve.rates)
        rates = [0] * l

        dt = self.curve.base.yearFraction(d1=val_date, d2=val_date + t, calendar=self.curve.calendar)

        dfT = self.curve.discount(val_date=val_date, date=val_date + t)[0]
        dftt = self.curve.discount(val_date=val_date, date=val_date + t + Days(1))[0]
        fm0t = -(log(dftt) - log(dfT)) * 365

        dfT = self.curve.discount(val_date=val_date, date=val_date + t)[0]
        dftt = self.curve.discount(val_date=val_date, date=val_date + t + Days(1))[0]
        fm0s = -(log(dftt) - log(dfT)) * 365

        alfat = fm0t + self.MRV ** 2 / (2 * self.MRS ** 2) * (1 - exp(-self.MRS * dt)) ** 2
        alfas = fm0s

        rs = self.curve.rates[0]

        ert = rs * exp(-self.MRS * dt) + alfat - alfas * exp(-self.MRS * dt)

        vart = self.MRV ** 2 / (2 * self.MRS) * (1 - exp(-2 * self.MRS * dt))

        rt = ert + sqrt(vart) * random

        for i in range(0, l):
            dtenor = self.curve.base.yearFraction(d1=val_date, d2=self.curve.dates[i], calendar=self.curve.calendar)
            BTT = 1 / self.MRS * (1 - exp(-self.MRS * dtenor))
            dfT = self.curve.discount(val_date=val_date, date=val_date + t)[0]
            dftt = self.curve.discount(val_date=val_date, date=self.curve.dates[i] + t)[0]
            AtT = dftt / dfT * exp(BTT * fm0t - self.MRV ** 2 / (4 * self.MRS) *
                                   (1 - exp(-2 * self.MRS * dt)) * BTT ** 2)
            PtT = AtT * exp(-BTT * rt)
            rates[i] = (1 / PtT) ** (365 / (self.curve.dates[i] - val_date)) - 1

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

    IPCA_m = HullWhite(curve=IPCA, MRV=0.0025, MRS=0.01, flag=True)
    print(IPCA_m.sim(val_date=valDate, t=Days(29), random=0.167728385139152))


