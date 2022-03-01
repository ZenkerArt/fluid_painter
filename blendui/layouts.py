from abc import ABC, abstractmethod

from .events import EventCatcherWidget
from .widgets import Widget


class Layout(Widget, ABC):
    _widgets: list[Widget]
    events: EventCatcherWidget
    _computed: bool = False

    def __init__(self):
        self._widgets = []
        self.events = EventCatcherWidget(self)

    def add_widget(self, widget: Widget):
        self._widgets.append(widget)

    @property
    def widgets(self):
        return self._widgets

    @abstractmethod
    def _compute(self):
        pass

    def compute(self):
        if self._computed:
            return
        self._compute()
        self._computed = True
        return self


class HLayout(Layout):
    _row_count: int = -1
    _margin: float = 10

    def _compute(self):
        row_count = self._row_count

        if row_count == -1:
            row_count = len(self._widgets)

        size = self._size[0] / row_count
        px, py = self._pos

        for index, widget in enumerate(self._widgets):
            size_x = size * index
            widget.set_pos(size_x + px, py)
            widget.set_size(size - self._margin, size - self._margin)
            if hasattr(widget, 'compute'):
                widget.compute()

    def set_row_count(self, value: int):
        self._row_count = value
        return self

    def set_gap(self, gap: float):
        self._margin = gap

    def draw(self):
        self.compute()
        for index, widget in enumerate(self._widgets):
            widget.draw()


class VLayout(Layout):
    _margin: float = 0

    def _calc_height(self, widget: Widget):
        return widget.height + self._margin

    def _compute(self):
        px, py = self._pos
        size_y = 0

        for index, widget in enumerate(self._widgets):
            widget.set_pos(px, py + size_y)
            widget.set_width(self.width)
            size_y += self._calc_height(widget)

            if hasattr(widget, 'compute'):
                widget.compute()

    def set_margin(self, margin: float):
        self._margin = margin

    @property
    def height(self):
        height = 0
        for widget in self._widgets:
            height += self._calc_height(widget)
        return height

    def draw(self):
        self.compute()

        for index, widget in enumerate(self._widgets):
            widget.draw()