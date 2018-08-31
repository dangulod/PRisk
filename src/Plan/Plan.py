from src.assets.products import Portfolio
from src.liabilities.liabilities import Liability
from src.dates.date import Date, Years, Periods


class Plan:
    def __init__(self, val_date: Date, t: Periods, liabilities: Liability, assets=Portfolio()):
        if not isinstance(liabilities, Liability):
            raise ValueError("liabilities must be class Liability class")
        if not isinstance(assets, Portfolio):
            raise ValueError("assets must be a Portfolio class")
        if not isinstance(t, Periods):
            raise ValueError("t is not a Period class")
        if not isinstance(val_date, Date):
            raise ValueError("t is not a Date class")
        self.assets      = assets
        self.liabilities = liabilities
        self.val_date    = val_date
        self.t           = t

    def GAP(self):
        return self.assets.NPV() - self.liabilities.PBO()

