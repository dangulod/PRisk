from src.dates.date import Date, Days, Years
from src.curves.curve import Curve, NullCurve, IRR
from src.dates.conventions import Actual365, Thirty360
from src.dates.calendar import Calendar

class Liability:
    def __init__(self, val_date: Date, dates, curve_irr: Curve, curve_spread=NullCurve(), curve_inf=NullCurve()):
        if not isinstance(val_date, Date):
            raise ValueError("val_date is not a Date class")
        if not isinstance(curve_irr, Curve) or not isinstance(curve_spread, Curve) or not isinstance(curve_inf, Curve):
            raise ValueError("IRR, spread, inflation curves must be a Curve class")
        self.val_date     = val_date
        self.dates        = dates
        self.curve_irr    = curve_irr
        self.curve_spread = curve_spread
        self.curve_inf    = curve_inf

    def PBO(self):
        pass


class Liabilities(Liability):
    def __init__(self, val_date: Date, dates, flows, curve_irr: Curve, curve_spread=NullCurve(), curve_inf=NullCurve()):
        if len(dates) != len(flows):
            raise ValueError("Dates and flows must have the same length")
        super().__init__(val_date=val_date, dates=dates, curve_irr=curve_irr, curve_spread=curve_spread,
                       curve_inf=curve_inf)
        self.flows    = flows
        self.duration = int(round(self.duration() * 365, 0))

    def __len__(self):
        return len(self.flows)

    def __str__(self):
        return "LIABILITIES with " + str(len(self)) + " years"

    def duration(self):
        irr = self.curve_irr.rate(self.dates)
        spread = self.curve_spread.rate(self.dates)

        l   = len(self.dates)
        d   = [0] * l
        td  = [0] * l
        num = 0
        den = 0

        for i in range(0, l): td[i] = Actual365.yearFraction(self.val_date, self.dates[i], Calendar())
        for i in range(0, l): d[i] = self.flows[i] / ((1 + irr[i] + spread[i]) ** td[i])
        for i in range(0, l): num += (d[i] * td[i])
        for i in range(0, l): den += d[i]

        return num / den

    def PBO(self):

        curve = self.curve_irr + self.curve_spread

        m      = self.val_date.month()
        inf    = self.curve_inf.rate(self.val_date + Days(self.duration))[0]
        r      = curve.rate(self.val_date + Days(self.duration))[0]

        l  = len(self.dates)
        d  = 0
        td = [0] * l

        for i in range(0, l): td[i] = Thirty360.yearFraction(self.dates[0], self.dates[i] + Years(1), Calendar())
        for i in range(0, l - 1):
           d += ((((12 - m) / 12) * self.flows[i] * (( 1 + inf) ** td[i]))  + \
                ((m / 12) * self.flows[i + 1] * ((1 + inf) ** td[i + 1]))) / \
                ((1 + r) ** (td[i] - 0.5))

        d += (((12 - m) / 12) * self.flows[l - 1] * (( 1 + inf) ** td[l - 1])) / \
                ((1 + r) ** td[l - 1])
        return d


class LiabilitiesUK(Liability):
    def __init__(self, val_date: Date, dates, active, deferred, pensioner, curve_irr: Curve, curve_spread=NullCurve(),
                 curve_inf=NullCurve()):
        if len(dates) != len(active) or len(dates) != len(deferred) or len(dates) != len(pensioner):
            raise ValueError("Dates and flows must have the same length")
        super().__init__(val_date=val_date, dates=dates, curve_irr=curve_irr, curve_spread=curve_spread,
                       curve_inf=curve_inf)
        self.active    = active
        self.deferred  = deferred
        self.pensioner = pensioner



if __name__ == "__main__":
    import pandas as pd
    from src.curves.curve import get_curve
    from src.dates.date import Days

    curves = pd.read_excel("../../data/Inputs_Pensiones.xlsx")
    curves.Tenor = curves.Tenor.apply(lambda x: Date(31, 12, 2017) + Days(x))

    curves = curves.groupby('Name'). \
        apply(lambda x: Curve(name=str(x.Name.unique()[0]),
                              dates=x.Tenor.tolist(),
                              rates=x.Rate.tolist()))

    Liabilities(val_date=Date(31,12,2017),
                dates=[Date(31,12, 2018), Date(31,12, 2019), Date(31,12, 2020)],
                flows=[1000, 2000, 3000],
                curve_irr=curves[0])

    l = pd.read_excel("../../data/Datos_20180531.xlsx", sheet_name='Pasivos_Pruebas', usecols='A:i')

    l[l.select_dtypes(include=['datetime']).columns] = \
        l[l.select_dtypes(include=['datetime']).columns]. \
            applymap(lambda x: Date(x.day, x.month, x.year))

    l = l.groupby(['Pais', 'Plan']). \
        apply(lambda x: Liabilities(val_date=Date(31,12, 2017), dates=x.FechaCF.tolist(),
                                    flows=x.CF.tolist(),
                                    curve_irr=get_curve(x.Curve.unique()[0], curves)))

    print(l[0].duration)
    print(l[0].PBO())

    LUK = pd.read_excel("../../UK/UK.xlsx", sheet_name="Liabilities")

    LiabilitiesUK(Date(31, 5, 2018), LUK.FechaCF, LUK.Active, LUK.Deferred, LUK.Pensioner, curves['iBoxx'])


