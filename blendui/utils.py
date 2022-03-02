from typing import Union

Number = Union[float, int]


class Color:
    _r: Number = 0
    _g: Number = 0
    _b: Number = 0
    _a: Number = 1

    def __init__(self, r: Number = 0, g: Number = 0, b: Number = 0, a: Number = 1):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    @classmethod
    def white(cls):
        return cls(1, 1, 1)

    @classmethod
    def black(cls):
        return cls()

    def alpha(self, value: Number):
        self._a = value
        return self

    def to_rgba(self) -> tuple[Number, Number, Number, Number]:
        return self._r, self._g, self._b, self._a

    def to_rgb(self) -> tuple[Number, Number, Number]:
        return self._r, self._g, self._b
