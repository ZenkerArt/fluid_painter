from abc import ABC, abstractmethod

import bgl
import blf
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from .mixin import WithColor


class Widget(ABC):
    _size: tuple[float, float] = (100, 100)
    _pos: tuple[float, float] = (0, 0)

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    def set_width(self, value: float):
        self._size = (value, self._size[1])
        return self

    def set_height(self, value: float):
        self._size = (self._size[0], value)
        return self

    def set_size(self, x: float, y: float):
        self._size = (x, y)
        return self

    def set_pos(self, x: float, y: float):
        self._pos = (x, y)
        return self

    @abstractmethod
    def draw(self):
        pass


class Rect(Widget, WithColor):
    _offset: tuple[float, float] = (0, 0)

    def set_offset(self, x: float, y: float):
        self._offset = (x, y)
        return self

    def draw(self):
        ox, oy = self._offset
        ox1, oy1 = ox / 2, oy / 2

        px, py = self._pos
        w, h = self._size

        px, py = px - ox1, py - oy1
        w, h = w + ox, h + oy

        vertices = (
            (px, py), (px + w, py),
            (px, py + h), (px + w, py + h))

        indices = (
            (0, 1, 2), (2, 1, 3))

        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

        shader.bind()
        shader.uniform_float("color", (self._color.to_rgba()))
        batch.draw(shader)


class Image(Widget):
    _image: bpy.types.Image

    def __init__(self, image: bpy.types.Image):
        self._image = image

    @property
    def height(self):
        sx, sy = self._size
        return sx

    def draw(self):
        x, y = self._pos
        sx, sy = self._size

        shader = gpu.shader.from_builtin('2D_IMAGE')
        sy = sx
        sx = sy

        batch = batch_for_shader(
            shader, 'TRI_FAN',
            {
                "pos": (
                    (x, y), (x + sx, y),
                    (x + sx, y + sy), (x, y + sy)
                ),
                "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
            },
        )

        bgl.glEnable(bgl.GL_BLEND)
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, self._image.bindcode)
        shader.bind()
        shader.uniform_int("image", 0)
        batch.draw(shader)


class Text(Widget, WithColor):
    _text: str = 'Hello World'
    _font_id: int = 0

    def set_text(self, text: str):
        self._text = text
        return self

    @property
    def width(self) -> int:
        return blf.dimensions(self._font_id, self._text)[0]

    def draw(self):
        font_id = 0
        blf.position(font_id, self.x, self.y, 0)
        blf.size(font_id, int(self.height), 72)
        blf.color(font_id, *self._color.to_rgba())
        blf.draw(font_id, self._text)
        # blf
