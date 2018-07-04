from src.dates.conventions import Thirty360, Actual360, Actual365, BUSS252

def get_base(argument):
    switcher = {
        "ACT/365" : Actual365(),
        "30/360"  : Thirty360(),
        "ACT/360" : Actual360(),
        "BUSS/252": BUSS252()
    }
    x = switcher.get(argument, None)
    if ( x == None ):
        raise ValueError("Invalid base argument")
    else:
        return x


