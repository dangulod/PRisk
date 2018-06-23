from src.dates.date import Date, Days

class Calendar:
    def __init__(self):
        pass

    def isHoliday(self, date):
        return self.isWeekend(date)

    def isBusinessDay(self, date):
        return not self.isHoliday(date)

    def isWeekend(self, date):
        return True if ( date.weekday() > 5 ) else False

    def isEndOfMonth(self, date):                   # Not implemented
        pass

    def nextBusinessDay(self, date):
        day = date
        while (self.isHoliday(day)):
            day += Days(1)
        return day

    def businessDaysBetween(self, date_from, date_to):
        if ( not isinstance(date_from, Date) or not isinstance(date_to, Date) ):
            raise ValueError("Input must be dates")

        natDays = date_to - date_from
        busDays = 0

        for i in range(1, natDays):
            busDays += self.isBusinessDay(date_from + Days(i))

        return busDays


if __name__ == "__main__":
    x = Calendar()
    print(x.businessDaysBetween(Date( 1, 1, 2018), Date( 1, 1, 2019)))
    y = x.nextBusinessDay(Date(22, 6, 2018))
    print(y)