from src.dates.date import Date, Years, isleap, Days
from src.dates.calendar import Calendar

class DayCounter:
    def __init__(self):
        pass

    @staticmethod
    def dayCount(d1, d2, calendar = None):
        if ( isinstance(d1, Date) and isinstance(d2, Date )):
            return d2 - d1

    @staticmethod
    def yearFraction(d1, d2, calendar = None):
        pass


class Thirty360(DayCounter):
    def __init__(self):
        pass

    @staticmethod
    def dayCount(d1, d2, calendar = None):   # EU_Implementation
        dd1 = d1.day()
        dd2 = d2.day()
        md1 = d1.month()
        md2 = d2.month()
        yy1 = d1.year()
        yy2 = d2.year()

        return 360 * (yy2 - yy1) + 30 * (md2 - md1 - 1) + max(int(0), 30 - dd1) + min(int(30), dd2);

    @staticmethod
    def yearFraction(d1, d2):
        return Thirty360.dayCount(d1, d2) / 360.0


class Actual360(DayCounter):
    def __init__(self):
        pass

    @staticmethod
    def yearFraction(d1, d2):
        return DayCounter.dayCount( d1, d2 ) / 360.0


class Actual365(DayCounter):
    def __init__(self):
        pass

    @staticmethod
    def yearFraction(d1, d2):
        return DayCounter.dayCount( d1, d2 ) / 365.0


class BUSS252(DayCounter):
    def __init__(self):
        pass

    @staticmethod
    def dayCount(d1, d2, calendar):
        isinstance(calendar, Calendar)
        return calendar.businessDaysBetween(d1, d2)

    @staticmethod
    def yearFraction(d1, d2, calendar):
        return BUSS252.dayCount(d1, d2, calendar) / 252


if __name__ == "__main__":
    from src.dates.calendars.Brazil import Brazil
    print(Thirty360.yearFraction(Date( 1, 1, 2013), Date( 1, 1, 2014)))
    print(Actual365.yearFraction(Date( 1, 1, 2013), Date( 1, 1, 2014)))
    print(Actual360.yearFraction(Date( 1, 1, 2013), Date( 1, 1, 2014)))
    print(BUSS252.yearFraction(Date( 1, 1, 2013), Date( 1, 1, 2014), calendar=Brazil()))
