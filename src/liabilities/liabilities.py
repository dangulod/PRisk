from src.dates.date import Date
from src.curves.curve import Curve, NullCurve, IRR
from src.dates.conventions import Actual365
from src.dates.calendar import Calendar

class Liabilities:
    def __init__(self, dates, flows, curve_irr: Curve, curve_spread=NullCurve(), curve_inf=NullCurve()):
        if len(dates) != len(flows):
            raise ValueError("Dates and flows must have the same length")
        self.dates  = dates
        self.flows  = flows
        self.curve_irr = curve_irr
        self.curve_spread = curve_spread
        self.curve_inf = curve_inf

    def duration(self, val_date: Date):
        irr = self.curve_irr.rate(self.dates)
        spread = self.curve_spread.rate(self.dates)

        l = len(irr)
        d = [0] * l
        td = [0] * l
        num = 0
        den = 0

        for i in range(0, l): td[i] = Actual365.yearFraction(val_date, self.dates[i], Calendar())
        for i in range(0, l): d[i] = self.flows[i] / ((1 + irr[i] + spread[i]) ** td[i])
        for i in range(0, l): num += (d[i] * td[i])
        for i in range(0, l): den += d[i]

        return num / den

    def PBO(self, val_date: Date):
        m = val_date.month()
        inf = self.curve_inf.rate(self.dates)
        irr = self.curve_irr.rate(self.dates)
        spread = self.curve_spread.rate(self.dates)

        l = len(irr)
        d = 0
        td = [0] * l

        for i in range(0, l): td[i] = Actual365.yearFraction(val_date, self.dates[i], Calendar())
        for i in range(0, l - 1):
            d += (((12 - m) /12) * self.flows[i] * (( 1 + inf[i]) ** td[i])) / \
                 ((1 + irr[i] + spread[i]) ** td[i]) + \
                 ((m / 12) * self.flows[i + 1] * ((1 + inf[i + 1]) ** td[i + 1])) / \
                 ((1 + irr[i + 1] + spread[i + 1]) ** td[i + 1])

        d += (((12 - m) / 12) * self.flows[l - 1] * (( 1 + inf[l - 1]) ** td[l - 1])) / \
                 ((1 + irr[l - 1] + spread[l - 1]) ** td[l - 1])
        return d


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

    l = pd.read_excel("../../data/Datos_20180531.xlsx", sheet_name='Pasivos_Pruebas', usecols='A:i')

    l[l.select_dtypes(include=['datetime']).columns] = \
        l[l.select_dtypes(include=['datetime']).columns]. \
            applymap(lambda x: Date(x.day, x.month, x.year))

    l = l.groupby(['Pais', 'Plan']). \
        apply(lambda x: Liabilities(dates=x.FechaCF.tolist(),
                                    flows=x.CF.tolist(),
                                    curve_irr=get_curve(x.Curve.unique()[0], curves)))

    print(l[0].duration(Date(31, 12, 2017)))
    print(l[0].NPV(Date(31, 12, 2017)))
