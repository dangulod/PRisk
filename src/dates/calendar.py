from src.dates.date import Date

class Calendar:
    def __init__(self):
        pass

    def isHoliday(self, date):
        return self.isWeekend(date)

    def isBusinessDay(self, date):
        return not self.Holiday()

    def isWeekend(self, date):
        return True if ( date.weekday() > 5 ) else False

    def isEndOfMonth(self, date):
        pass


if __name__ == "__main__":
    pass
