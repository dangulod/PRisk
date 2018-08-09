from src.utils.utils import where


class Factor:
    def __init__(self, name, factor=1):
        self.name   = name
        self.factor = [factor]

    def getFactor(self):
        return self.factor[0]

    def __str__(self):
        return "Factor " + str(self.name)

    def __repr__(self):
        return "Factor " + str(self.name)


class NullFactor(Factor):
    def __init__(self):
        pass

    def __str__(self):
        return "NullFactor"

    def __repr__(self):
        return "NullFactor"


def copy_factor(factor_from: Factor):
    if not isinstance(factor_from, Factor):
        raise ValueError("factor_from must be a list")
    return Factor(name=factor_from.name, factor=factor_from.getFactor())


def get_factor(name, array):
    if ( name == "None" or str(name) == "nan"):
        return NullFactor()
    try:
        return array[where(array.map(lambda x: x.name), name)]
    except ValueError:
        raise ValueError("factor %s not found" % name)


if __name__ == "__main__":
    EQ1 = Factor(name="EQ1")
    print(EQ1.name)
    print(copy_factor(EQ1).name)


