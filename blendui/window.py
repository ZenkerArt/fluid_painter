import ctypes

import bpy

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class Window:
    _region: bpy.types.Region
    _ui: bpy.types.Region

    def __init__(self, region: bpy.types.Region, ui: bpy.types.Region):
        self._region = region
        self._ui = ui

    @property
    def scale(self):
        scale = self.width / screensize[0]
        return scale

    @property
    def width(self) -> int:
        return self._region.width - self._ui.width

    @property
    def height(self) -> int:
        return self._region.height
