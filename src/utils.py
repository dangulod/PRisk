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


def ClassFactory(name, argnames, BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the
            # ClassFactory call
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name[:-len("Class")])
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass

if __name__ == "__main__":
    from src.Assets.Products import Bond

    x = Bond()