from src.curves.curve import Curve, NullCurve
from src.simulation.factor import Factor, NullFactor
from src.utils.utils import find


class Scenario:
    def __init__(self, factors: list, curves: list):
        self.factors = factors
        self.curves  = curves

    def getCuNames(self):
        return list(map(lambda x: x.name, self.curves))

    def getFaNames(self):
        return list(map(lambda x: x.name, self.factors))

    def getFactor(self, name: str):
        return self.factors[find(self.getFaNames(), name)]

    def getCurve(self, name: str):
        return self.curves[find(self.getCuNames(), name)]


if __name__ == "__main__":
    from src.dates.date import Date, Days

    factors = [Factor(name="EQ1")] + [Factor(name="EQ2")] + [Factor(name="EQ3")]

    val_date = Date(31, 12, 2017)

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

    curves = [IT_BOND] + [PT_BOND] + [ES_BOND]

    s = Scenario(factors=factors, curves=curves)
    print(s.getCurve("ES_BOND"))
