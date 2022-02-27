class ColorRGBA:
    _r: float = 0
    _g: float = 0
    _b: float = 0
    _a: float = 1

    def rgb(self, value: tuple[float, float, float]):
        self._r, self._g, self._b = value
        return self

    def alpha(self, value: float):
        self._a = value
        return self

    def to_rgba(self) -> tuple[float, float, float, float]:
        return self._r, self._g, self._b, self._a

    def to_rgb(self) -> tuple[float, float, float]:
        return self._r, self._g, self._b
