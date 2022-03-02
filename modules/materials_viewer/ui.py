from dataclasses import dataclass

import bpy
from .material_list import MaterialsViewerItem
from ...assets import Assets
from ...blendui.utils import Color
from ...blendui.window import Window
from ...blendui.widgets import Text, Image, Rect
from ...blendui.layouts import VLayout, HLayout


def build_preview_mat(
        window: Window,
        image: bpy.types.Image,
):
    scale = window.scale

    p = VLayout()
    p.set_margin(-scale * 50)

    preview_mat = VLayout()
    preview_mat.set_margin(scale * 50)
    preview_mat.add_widget(Image(image))

    p.add_widget(preview_mat)

    return p


def build_preview_popup(
        window: Window,
        label: str,
        subtitle: str,
        image: bpy.types.Image
):
    scale = window.scale

    preview_mat = VLayout()

    texts = VLayout()
    texts.set_margin(scale * 40)
    texts.add_widget(
        Text()
            .set_text(subtitle)
            .set_height(scale * 25)
            .set_color(Color.white())
            .set_alpha(.5))
    texts.add_widget(
        Text()
            .set_text(label)
            .set_height(scale * 35)
            .set_color(Color.white())
    )

    preview_mat.add_widget(texts)
    preview_mat.add_widget(Image(image))

    preview_mat.set_width(scale * 400)

    return preview_mat


class MaterialsViewer:
    window: Window = None
    _layout: HLayout
    _scroll: int = 0
    _items_count: int = 8
    _materials: list[MaterialsViewerItem]

    def __init__(self):
        self._materials = []

    def init(self):
        window = self.window
        self._layout = HLayout()

        self._layout.set_row_count(self._items_count)
        self._layout.set_pos(self.margin, 50 * window.scale)
        self._layout.set_width(window.width - self.margin / 2)
        self._layout.set_gap(self.margin + 20 * window.scale)

    @property
    def materials(self):
        return self._materials

    @materials.setter
    def materials(self, value: list[MaterialsViewerItem]):
        self._materials = value

    @property
    def materials_scroll(self) -> list[MaterialsViewerItem]:
        return self.materials[self._scroll:self._scroll + self._items_count]

    @property
    def margin(self):
        return 50 * self.window.scale

    @property
    def image_size(self):
        return 70 * self.window.scale

    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value: int):
        if value < 0:
            return

        if value > len(self.materials) - self._items_count:
            return
        self._scroll = value

    def draw(self):
        if self.window is None:
            raise RuntimeError('Window is None!')

        Assets.load()
        layout = self._layout
        margin = self.margin
        image_size = self.image_size

        for fluid_mat in self.materials_scroll:
            self._layout.add_widget(build_preview_mat(
                self.window,
                fluid_mat.image
            ))

        self._layout.compute()

        for wid in layout.widgets:
            Rect() \
                .set_pos(wid.x, wid.y) \
                .set_size(wid.width, wid.height) \
                .set_offset(margin + 2, margin + 4) \
                .set_color(Color.black()) \
                .draw()

            Rect() \
                .set_pos(wid.x, wid.y) \
                .set_size(wid.width, wid.height) \
                .set_offset(margin, margin) \
                .set_color(Color(.15, .15, .15)) \
                .draw()

            Image(Assets.fluid_logo_black) \
                .set_pos(wid.x - image_size / 2, wid.y - image_size / 2) \
                .set_size(wid.width + image_size, wid.width + image_size) \
                .draw()
        layout.draw()

        return layout
