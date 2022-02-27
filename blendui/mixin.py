from .utils import ColorRGBA


class WithColor:
    _color: ColorRGBA

    def __init__(self):
        self._color = ColorRGBA()

    def set_color(self, r: float, g: float, b: float):
        self._color.rgb((r, g, b))
        return self

    def set_alpha(self, value: int):
        self._color.alpha(value)
        return self