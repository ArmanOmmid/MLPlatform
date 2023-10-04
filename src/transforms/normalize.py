
class NormalizeDivide:
    def __init__(self, denominator: float):
        self.denominator = float(denominator)

    def __call__(self, x):
        return x / self.denominator
