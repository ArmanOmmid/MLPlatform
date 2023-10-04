
class RGB:
    @classmethod
    def __call__(cls, x):
        return x.repeat(3, 1, 1) if input.size(0) == 1 else x

class Permute:
    def __init__(self, *order: int):
        self.order = order

    def __call__(self, x):
        return x.permute(*self.order)
