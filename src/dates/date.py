def minSerialNumber():
    return 366             # Jan 1st, 1901


def maxSerialNumber():
    return 109574           # Dec 31st, 2199


def checkSerialNumber(date):
    if ( date <  minSerialNumber() or date > maxSerialNumber() ):
        raise ValueError("Date's serial number outside of range")


def isleap(y):
    leap = (
        # 1900-1909
        False, False, False, False, True, False, False, False, True, False,
        # 1910-1919
        False, False, True, False, False, False, True, False, False, False,
        # 1920-1929
        True, False, False, False, True, False, False, False, True, False,
        # 1930-1939
        False, False, True, False, False, False, True, False, False, False,
        # 1940-1949
        True, False, False, False, True, False, False, False, True, False,
        # 1950-1959
        False, False, True, False, False, False, True, False, False, False,
        # 1960-1969
        True, False, False, False, True, False, False, False, True, False,
        # 1970-1979
        False, False, True, False, False, False, True, False, False, False,
        # 1980-1989
        True, False, False, False, True, False, False, False, True, False,
        # 1990-1999
        False, False, True, False, False, False, True, False, False, False,
        # 2000-2009
        True, False, False, False, True, False, False, False, True, False,
        # 2010-2019
        False, False, True, False, False, False, True, False, False, False,
        # 2020-2029
        True, False, False, False, True, False, False, False, True, False,
        # 2030-2039
        False, False, True, False, False, False, True, False, False, False,
        # 2040-2049
        True, False, False, False, True, False, False, False, True, False,
        # 2050-2059
        False, False, True, False, False, False, True, False, False, False,
        # 2060-2069
        True, False, False, False, True, False, False, False, True, False,
        # 2070-2079
        False, False, True, False, False, False, True, False, False, False,
        # 2080-2089
        True, False, False, False, True, False, False, False, True, False,
        # 2090-2099
        False, False, True, False, False, False, True, False, False, False,
        # 2100-2109
        False, False, False, False, True, False, False, False, True, False,
        # 2110-2119
        False, False, True, False, False, False, True, False, False, False,
        # 2120-2129
        True, False, False, False, True, False, False, False, True, False,
        # 2130-2139
        False, False, True, False, False, False, True, False, False, False,
        # 2140-2149
        True, False, False, False, True, False, False, False, True, False,
        # 2150-2159
        False, False, True, False, False, False, True, False, False, False,
        # 2160-2169
        True, False, False, False, True, False, False, False, True, False,
        # 2170-2179
        False, False, True, False, False, False, True, False, False, False,
        # 2180-2189
        True, False, False, False, True, False, False, False, True, False,
        # 2190-2199
        False, False, True, False, False, False, True, False, False, False,
        # 2200
        False
    )
    return leap[ y - 1900 ]


mn = (  0,  31,  59,  90, 120, 151,             # Jan - Jun
      181, 212, 243, 273, 304, 334,             # Jun - Dec
      365 )


ml = (  0,  31,  60,  91, 121, 152,             # Jan - Jun
      182, 213, 244, 274, 305, 335,             # Jun - Dec
      366 )


def monthOffset(month, leap):
    if leap:
        return ml[month - 1]
    else:
        return mn[month - 1]


serial = (
            0,    365,    730,   1095,   1460,   1826,   2191,   2556,
         2921,   3287,   3652,   4017,   4382,   4748,   5113,   5478,
         5843,   6209,   6574,   6939,   7304,   7670,   8035,   8400,
         8765,   9131,   9496,   9861,  10226,  10592,  10957,  11322,
        11687,  12053,  12418,  12783,  13148,  13514,  13879,  14244,
        14609,  14975,  15340,  15705,  16070,  16436,  16801,  17166,
        17531,  17897,  18262,  18627,  18992,  19358,  19723,  20088,
        20453,  20819,  21184,  21549,  21914,  22280,  22645,  23010,
        23375,  23741,  24106,  24471,  24836,  25202,  25567,  25932,
        26297,  26663,  27028,  27393,  27758,  28124,  28489,  28854,
        29219,  29585,  29950,  30315,  30680,  31046,  31411,  31776,
        32141,  32507,  32872,  33237,  33602,  33968,  34333,  34698,
        35063,  35429,  35794,  36159,  36524,  36890,  37255,  37620,
        37985,  38351,  38716,  39081,  39446,  39812,  40177,  40542,
        40907,  41273,  41638,  42003,  42368,  42734,  43099,  43464,
        43829,  44195,  44560,  44925,  45290,  45656,  46021,  46386,
        46751,  47117,  47482,  47847,  48212,  48578,  48943,  49308,
        49673,  50039,  50404,  50769,  51134,  51500,  51865,  52230,
        52595,  52961,  53326,  53691,  54056,  54422,  54787,  55152,
        55517,  55883,  56248,  56613,  56978,  57344,  57709,  58074,
        58439,  58805,  59170,  59535,  59900,  60266,  60631,  60996,
        61361,  61727,  62092,  62457,  62822,  63188,  63553,  63918,
        64283,  64649,  65014,  65379,  65744,  66110,  66475,  66840,
        67205,  67571,  67936,  68301,  68666,  69032,  69397,  69762,
        70127,  70493,  70858,  71223,  71588,  71954,  72319,  72684,
        73049,  73414,  73779,  74144,  74509,  74875,  75240,  75605,
        75970,  76336,  76701,  77066,  77431,  77797,  78162,  78527,
        78892,  79258,  79623,  79988,  80353,  80719,  81084,  81449,
        81814,  82180,  82545,  82910,  83275,  83641,  84006,  84371,
        84736,  85102,  85467,  85832,  86197,  86563,  86928,  87293,
        87658,  88024,  88389,  88754,  89119,  89485,  89850,  90215,
        90580,  90946,  91311,  91676,  92041,  92407,  92772,  93137,
        93502,  93868,  94233,  94598,  94963,  95329,  95694,  96059,
        96424,  96790,  97155,  97520,  97885,  98251,  98616,  98981,
        99346,  99712, 100077, 100442, 100807, 101173, 101538, 101903,
       102268, 102634, 102999, 103364, 103729, 104095, 104460, 104825,
       105190, 105556, 105921, 106286, 106651, 107017, 107382, 107747,
       108112, 108478, 108843, 109208, 109573
    )


def yearOffset(year):
    return serial[ year - 1900 ]


def monthLength(month, leap):
    if leap:
        l = ( 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 )
    else:
        l = ( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 )
    return l[ month - 1 ]


class Date:
    def __init__(self,  day,  month,  year):
        if ( (not isinstance(day,  int)) | (not isinstance(month,  int)) | (not isinstance(year,  int)) ):
            raise  ValueError( "Year,  month & day must be integers" )
        if ( month < 1 or month > 12 ):
            raise ValueError( "Month out of bound. It must be in [1-12]" )
        if ( year < 1900 or year > 2200 ):
            raise ValueError( "Year out of bound. It must be in [1900-2200]" )

        leap = isleap(year)
        leng = monthLength(month, leap)

        if ( day < 1 or day > leng ):
            raise  ValueError( "Day out of bound" )

        offset = monthOffset(month, leap)
        s = day + offset + yearOffset(year)
        checkSerialNumber(s)
        self.serialNumber = s

    def year(self):
        i = 0
        while (self.serialNumber > serial[i]):
            i += 1
        return 1899 + i

    def month(self):
        i    = 0
        y    = self.year()
        leap = isleap(y)
        day  = self.dayOfYear()
        if leap:
            while ( day > ml[i] ) : i += 1
        else:
            while ( day > mn[i] ) : i += 1
        return i

    def day(self):
        y = self.year()
        l = isleap(y)
        m = self.month()
        d = self.dayOfYear()

        return d - monthOffset(m, l)

    def dayOfYear(self):
        return self.serialNumber - yearOffset(self.year())

    def weekday(self):
        wday = self.serialNumber % 7
        return wday if wday != 0 else 7

    def __eq__(self, other):
        if isinstance(other, Date):
            return self.serialNumber == other.serialNumber
        else:
            raise ValueError("Date must be compared with Dates")

    def __add__(self, other):
        if isinstance(other, Days):
            return serialToDate( self.serialNumber + other.d )
        if isinstance(other, Weeks):
            return serialToDate( self.serialNumber + other.w * 7 )
        if isinstance(other, Months):
            y = self.year()
            m = self.month()
            d = self.day()
            i = m - 1 + other.m
            m = i % 12 + 1
            y = y + i / 12
            days = monthLength( m, isleap(int(y)) )
            if ( d > days ): d = days
            return Date( int(d), int(m), int(y) )
        if isinstance(other, Quarter):
            return self + Months(other.q * 3)
        if isinstance(other, Semesters):
            return self + Months(other.s * 6)
        if isinstance(other, Years):
            return self + Months(other.y * 12)

    def __sub__(self, other):
        if isinstance(other, Date):
            return self.serialNumber - other.serialNumber
        if isinstance(other, Days):
            return serialToDate( self.serialNumber - other.d )
        if isinstance(other, Months):
            y = self.year()
            m = self.month()
            d = self.day()
            i = m - 1 - other.m
            m = i % 12 + 1
            y = y + i / 12
            days = monthLength(m, isleap(int(y)))
            if (d > days): d = days
            return Date(int(d), int(m), int(y))
        if isinstance(other, Quarter):
            return self - Months(other.q * 4)
        if isinstance(other, Semesters):
            return self - Months(other.s *6)
        if isinstance(other, Years):
            return self - Months(other.y * 12)

    def __str__(self):
        return str(self.day()) + "-" + str(self.month()) + "-" + str(self.year())


def serialToDate(serialNumber):
    # Year
    i = 0
    while (serialNumber > serial[i]):
        i += 1
    year = 1899 + i
    # Month
    i = 0
    leap = isleap(year)
    doy = serialNumber - yearOffset(year)
    if leap:
        while (doy > ml[i]): i += 1
    else:
        while (doy > mn[i]): i += 1
    month = i
    # Day
    day = doy - monthOffset(month, leap)
    return Date(day, month, year)


class Days:
    def __init__(self, d):
        if (( not isinstance(d, int) or not d > 0 )):
            raise ValueError("d must be a positive integer")
        self.d = d


class Weeks:
    def __init__(self, w):
        if (( not isinstance(w, int) or not w > 0 )):
            raise ValueError("w must be a positive integer")
        self.w = w


class Months:
    def __init__(self, m):
        if (( not isinstance(m, int) or not m > 0 )):
            raise ValueError("m must be a positive integer")
        self.m = m


class Quarter:
    def __init__(self, q):
        if (( not isinstance(q, int) or not q > 0 )):
            raise ValueError("q must be a positive integer")
        self.q = q


class Semesters:
    def __init__(self, s):
        if (( not isinstance(s, int) or not s > 0 )):
            raise ValueError("s must be a positive integer")
        self.s = s


class Years:
    def __init__(self, y):
        if (( not isinstance(y, int) or not y > 0 )):
            raise ValueError("y must be a positive integer")
        self.y = y


if __name__ == "__main__":
    x = Date(31, 3, 2012)
    print( x - Months(1) == Date(29, 2, 2012))