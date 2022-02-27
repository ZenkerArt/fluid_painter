import enum
import os
import random
from abc import ABC, abstractmethod

import bgl
import blf
import bpy
import gpu
from ...assets import load, get_pics
from gpu_extras.batch import batch_for_shader
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

handlers = []
IMAGES_PATH = r'C:\Users\ll\Desktop\blender_projects\addons\fluid_painter\files\Pics'


# def point_rect_colliding(r1, r2):
#     return not (r1.x>r2.x+r2.w or r1.x+r1.w<r2.x or r1.y>r2.y+r2.h or r1.y+r1.h<r2.y)


class EventCatcher:
    mouse_pos: tuple[int, int] = (0, 0)
    mouse_offset: tuple[int, int] = (0, 0)
    is_running: bool = False

    @classmethod
    def mouse_pos_relative(cls):
        x1, y1 = cls.mouse_pos
        x2, y2 = cls.mouse_offset
        return x1 - x2, y1 - y2

    @classmethod
    def event(cls, event: bpy.types.Event):
        cls.mouse_pos = (event.mouse_x, event.mouse_y)
        tag_redraw()

    @classmethod
    def run(cls):
        cls.is_running = True
        bpy.ops.fluidp.event_catcher('INVOKE_DEFAULT')

    @classmethod
    def stop(cls):
        cls.is_running = False


class EventCatcherWidget:
    _widget: 'Widget'

    def __init__(self, widget: 'Widget'):
        self._widget = widget

    def is_hover(self):
        x, y, w, h = self._widget.x, self._widget.y, self._widget.width, self._widget.height
        mx, my = EventCatcher.mouse_pos_relative()
        cx = x > mx or x + w < mx
        cy = y > my or y + h < my
        # print(y)

        if cx or cy:
            return False
        return True


def get_region(context) -> bpy.types.Region:
    for area in context.screen.areas:
        if area.type != 'VIEW_3D':
            continue

        for region in area.regions:
            if region.type == 'WINDOW':
                return region
    return None


def get_ui(context):
    for area in context.screen.areas:
        if area.type != 'VIEW_3D':
            continue

        for region in area.regions:
            if region.type == 'UI':
                return region
    return None


def tag_redraw():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()


class MaterialDrawSettings(bpy.types.PropertyGroup):
    row_count: bpy.props.IntProperty(default=5)


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


class Window:
    _region: bpy.types.Region

    def __init__(self, region: bpy.types.Region, ui: bpy.types.Region):
        self._region = region
        self._ui = ui

    @property
    def width(self) -> int:
        return self._region.width - self._ui.width

    @property
    def height(self) -> int:
        return self._region.height


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


class Text(Widget):
    _text: str = 'Hello World'
    _font_id: int = 0
    _color: ColorRGBA

    def __init__(self):
        self._color = ColorRGBA()

    def set_color(self, r: int, g: int, b: int):
        self._color.rgb((r, g, b))
        return self

    def set_alpha(self, value: float):
        self._color.alpha(value)
        return self

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


class FLUIDP_OT_event_catcher(bpy.types.Operator):
    bl_idname = "fluidp.event_catcher"
    bl_label = "Event catcher not for run!"
    bl_options = {'REGISTER'}

    def modal(self, context: bpy.types.Event, event: bpy.types.Event):
        EventCatcher.event(event)

        if not EventCatcher.is_running:
            EventCatcher.is_running = False
            return {'CANCELLED'}

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class FLUIDP_OT_draw_material(bpy.types.Operator):
    bl_label = 'draw_material'
    bl_idname = 'fluidp.draw_material'

    def execute(self, context: bpy.types.Context):
        logo_white, logo_1 = load()
        white = (255, 255, 255)
        images = get_pics()

        # for i in os.scandir(IMAGES_PATH):
        #     image = bpy.data.images.load(i.path, check_existing=True)
        #     image.gl_load()
        #     images.append(image)

        def draw():
            region = get_region(context)
            ui = get_ui(context)
            window = Window(region, ui=ui)
            scale = window.width / screensize[0]

            if region != context.region:
                return

            EventCatcher.mouse_offset = (region.x, region.y)
            preview_font_size = scale * 20

            def build_preview_mat(label: str, b_image: bpy.types.Image):
                p = VLayout()
                p.set_margin(-scale * 50)

                preview_mat = VLayout()
                preview_mat.set_margin(scale * 50)
                preview_mat.add_widget(Text()
                                       .set_text(label)
                                       .set_height(preview_font_size)
                                       .set_color(.8, .8, .8))
                preview_mat.add_widget(Image(b_image))

                p.add_widget(preview_mat)

                return p

            def build_preview_popup(label: str, b_image: bpy.types.Image):
                preview_mat = VLayout()
                # preview_mat.set_margin(-scale * 25)

                texts = VLayout()
                texts.set_margin(scale * 40)
                texts.add_widget(
                    Text()
                        .set_text('By Mike3DX')
                        .set_height(scale * 25)
                        .set_color(255, 255, 255)
                        .set_alpha(.5))
                texts.add_widget(Text().set_text(label).set_height(scale * 35).set_color(*white))

                preview_mat.add_widget(texts)
                preview_mat.add_widget(Image(b_image))

                preview_mat.set_width(scale * 400)

                return preview_mat

            items_count = 8
            offset = 50 * scale
            bg_size = 70 * scale
            layout = HLayout()
            layout.set_pos(offset, 50 * scale)
            layout.set_width(window.width - offset / 2)
            layout.set_gap(offset + 20 * scale)

            for img in images[:items_count]:
                name = ' '.join(img.name.rsplit('.')[0].split('_'))
                layout.add_widget(build_preview_mat(name, img))

            layout.compute()

            for wid in layout.widgets:
                Rect() \
                    .set_pos(wid.x, wid.y) \
                    .set_size(wid.width, wid.height) \
                    .set_offset(offset + 2, offset + 4) \
                    .set_color(0, 0, 0) \
                    .draw()

                Rect() \
                    .set_pos(wid.x, wid.y) \
                    .set_size(wid.width, wid.height) \
                    .set_offset(offset, offset) \
                    .set_color(.15, .15, .15) \
                    .draw()

                Image(logo_1) \
                    .set_pos(wid.x - bg_size / 2, (wid.y + 60 * scale) - bg_size / 2) \
                    .set_size(wid.width + bg_size, wid.width + bg_size) \
                    .draw()

                Rect() \
                    .set_pos(wid.x, wid.y) \
                    .set_size(wid.width, preview_font_size) \
                    .set_offset(offset, offset) \
                    .set_color(.1, .1, .1) \
                    .draw()

            layout.draw()

            popup_offset = 140 * scale

            for index, wid in enumerate(layout.widgets):
                if wid.events.is_hover():
                    img = images[index]
                    name = ' '.join(img.name.rsplit('.')[0].split('_'))

                    popup = build_preview_popup(name, img)
                    popup.set_width(wid.width * 1.5)
                    popup.set_pos(wid.x - offset / 2 + popup_offset / 2,
                                  wid.y + wid.height + offset / 2 + popup_offset / 2 + 20 * scale)
                    popup.compute()

                    Rect() \
                        .set_pos(popup.x, popup.y) \
                        .set_size(popup.width, popup.height) \
                        .set_offset(popup_offset, popup_offset) \
                        .set_color(.1, .1, .1) \
                        .draw()

                    popup.draw()

        draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')
        EventCatcher.run()
        handlers.append(draw_handler)
        tag_redraw()
        return {'FINISHED'}


class FLUIDP_OT_undraw_material(bpy.types.Operator):
    bl_label = 'undraw_material'
    bl_idname = 'fluidp.undraw_material'

    def execute(self, context: bpy.types.Context):
        for index, handler in enumerate(handlers):
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        handlers.clear()
        EventCatcher.stop()

        tag_redraw()

        return {'FINISHED'}


class FLUIDP_PT_material_selector(bpy.types.Panel):
    bl_label = 'Material'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fluid Painter'

    def draw(self, context: bpy.types.Context):
        self.layout.operator(FLUIDP_OT_draw_material.bl_idname)
        self.layout.operator(FLUIDP_OT_undraw_material.bl_idname)


classes = [FLUIDP_OT_draw_material, FLUIDP_OT_undraw_material, FLUIDP_PT_material_selector, FLUIDP_OT_event_catcher]
