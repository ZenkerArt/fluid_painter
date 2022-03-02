from .utils import Color


class WithColor:
    _color: Color

    def __init__(self):
        self._color = Color()

    def set_color(self, color: Color):
        self._color = color
        return self

    def set_alpha(self, value: int):
        self._color.alpha(value)
        return self