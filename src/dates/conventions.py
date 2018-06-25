from src.dates.date import Date

class DayCounter:
    def __init__(self):
        pass

    def dayCount(self, d1, d2):
        if ( isinstance(d1, Date) and isinstance(d2, Date )):
            return d2 - d1

    def yearFraction(self, d1, d2):
        pass


class Actual360(DayCounter):
    def __init__(self):
        pass

    def yearFraction(self, d1, d2):
        return self.dayCount( d1, d2 ) / 360.0


class Actual365(DayCounter):
    def __init__(self):
        pass

    def yearFraction(self, d1, d2):
        return self.dayCount( d1, d2 ) / 360.0