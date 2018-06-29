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

    def businessDaysBetween(self, date_from : Date, date_to : Date):
        if ( not isinstance(date_from, Date) or not isinstance(date_to, Date) ):
            raise ValueError("Input must be dates")

        nd = date_to - date_from
        sd = date_from.weekday()
        ed = date_to.weekday()

        nw = (((date_to - Days(ed - 1)) - (date_from - Days(sd - 1))) / 7) - 1

        return int(nd - nw * 2 - min(8 - sd, 2) - max(ed - 6, 0))

    def businessDaysBetween2(self, date_from, date_to):
        if (not isinstance(date_from, Date) or not isinstance(date_to, Date)):
            raise ValueError("Input must be dates")

        natDays = date_to - date_from
        busDays = 0

        for i in range(0, natDays):
            busDays += self.isBusinessDay(date_from + Days(i))

        return busDays



if __name__ == "__main__":
    x = Calendar()
    print(x.businessDaysBetween(Date( 23, 6, 2018), Date( 5, 7, 2018)))
    print(x.businessDaysBetween(Date( 1, 1, 2018), Date(1, 1, 2019)))
    print(x.businessDaysBetween2(Date(1, 1, 2018), Date(1, 1, 2019)))