from src.dates.conventions import Thirty360, Actual360, Actual365, BUSS252

def which(x, a):
    for i in range(0, len(x)):
        if (x[i] > a): return i

def where(x, a):
    for i in x:
        if (x[i] == a): return i
    raise ValueError("Value not found")

def split(df, group):
    gb = df.groupby(group)
    return [gb.get_group(x) for x in gb.groups]


def get_base(argument):
    switcher = {
        "ACT/365" : Actual365(),
        "30/360"  : Thirty360(),
        "ACT/360" : Actual360(),
        "BUSS/252": BUSS252()
    }
    x = switcher.get(argument, None)
    if ( x == None ):
        raise ValueError("Invalid argument")
    else:
        return x


def get_curve(name, array):
    return array[where(array.map(lambda x: x.name), name)]


if __name__ == "__main__":

    import src.assets.products as pricers
    from src.assets.products import Portfolio
    from src.dates.date import Date, Days
    from src.curves.curve import Curve, NullCurve

    p = Portfolio()
    valDate = Date(31, 12, 2017)

    ES_BOND = Curve(name="ES_BOND",
                    dates=[valDate + Days(360), valDate + Days(1080), valDate + Days(1440), valDate + Days(1800),
                           valDate + Days(2520), valDate + Days(3240), valDate + Days(3600), valDate + Days(5400),
                           valDate + Days(5580), valDate + Days(7200)],
                    rates=[-0.00528, -0.00024, 0.0006, 0.0037, 0.00819,
                           0.01322, 0.01558, 0.02225, 0.0223, 0.02361])

    class_ = getattr(pricers, "Bond")

    args = {'nominal': 4776736, 'startDate': Date(4, 3, 2015), 'matDate': Date(30, 7, 2030),
            'curve_irr': ES_BOND, 'coupon': 0.0178246127679505, 'curve_spread': NullCurve(),
            'frequency': 1, 'base':'ACT/365'}

    x1 = getattr(pricers, "Bond")(**args)

