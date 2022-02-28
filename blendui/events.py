import bpy
from .widgets import Widget


class EventCatcher:
    mouse_pos: tuple[int, int] = (0, 0)
    mouse_offset: tuple[int, int] = (0, 0)
    is_press: bool = False
    is_running: bool = False
    widgets: list['EventCatcherWidget'] = []

    @classmethod
    def reset(cls):
        pass

    @classmethod
    def mouse_pos_relative(cls):
        x1, y1 = cls.mouse_pos
        x2, y2 = cls.mouse_offset
        return x1 - x2, y1 - y2

    @classmethod
    def event(cls, event: bpy.types.Event):
        cls.mouse_pos = (event.mouse_x, event.mouse_y)
        cls.is_press = event.type == 'LEFTMOUSE'
        # if event.type == 'LEFTMOUSE':

    @classmethod
    def run(cls):
        cls.is_running = True
        bpy.ops.fluidp.event_catcher('INVOKE_DEFAULT')

    @classmethod
    def stop(cls):
        cls.is_running = False


class EventCatcherWidget:
    _widget: 'Widget'
    _is_click: bool = False

    def __init__(self, widget: 'Widget'):
        self._widget = widget
        EventCatcher.widgets.append(self)

    def is_hover(self):
        x, y, w, h = self._widget.x, self._widget.y, self._widget.width, self._widget.height
        mx, my = EventCatcher.mouse_pos_relative()
        cx = x > mx or x + w < mx
        cy = y > my or y + h < my

        if cx or cy:
            return False

        return True
