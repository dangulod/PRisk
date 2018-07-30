from src.assets.products import Portfolio
from src.liabilities.liabilities import Liabilities
from src.dates.date import Date, Years


class Plan:
    def __init__(self, liabilities: Liabilities, assets=Portfolio()):
        if not isinstance(liabilities, Liabilities):
            raise ValueError("liabilities must be class Liability class")
        if not isinstance(assets, Portfolio):
            raise ValueError("assets must be a Portfolio class")
        self.assets = assets
        self.liabilities = liabilities

    def GAP(self, val_date: Date, t=Years(1)):
        return self.assets.NPV(val_date=val_date, t=t) - self.liabilities.PBO(val_date)

