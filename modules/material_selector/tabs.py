import ctypes

import bpy
from .ui import build_preview_mat, build_preview_popup
from .utils import get_regions, tag_redraw
from ...assets import load, get_pics
from ...blendui.events import EventCatcher
from ...blendui.layouts import VLayout, HLayout
from ...blendui.widgets import Text, Image, Rect
from ...blendui.window import Window

handlers = []


class MaterialDrawSettings(bpy.types.PropertyGroup):
    row_count: bpy.props.IntProperty(default=5)


class FLUIDP_OT_event_catcher(bpy.types.Operator):
    bl_idname = "fluidp.event_catcher"
    bl_label = "Event catcher not for run!"
    bl_options = {'REGISTER'}

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        region, ui = get_regions(context)
        EventCatcher.event(event)

        if not EventCatcher.is_running:
            EventCatcher.is_running = False
            return {'CANCELLED'}
        tag_redraw(context)
        EventCatcher.mouse_offset = (region.x, region.y)

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class FLUIDP_OT_draw_material(bpy.types.Operator):
    bl_label = 'draw_material'
    bl_idname = 'fluidp.draw_material'

    def execute(self, context: bpy.types.Context):
        logo_white, logo_1 = load()
        images = get_pics()

        def draw():
            region, ui = get_regions(context)
            window = Window(region, ui)
            scale = window.scale

            if region != context.region:
                return

            preview_font_size = scale * 20

            items_count = 8
            offset = 50 * scale
            bg_size = 70 * scale
            layout = HLayout()
            layout.set_pos(offset, 50 * scale)
            layout.set_width(window.width - offset / 2)
            layout.set_gap(offset + 20 * scale)

            for img in images[:items_count]:
                name = ' '.join(img.name.rsplit('.')[0].split('_'))
                layout.add_widget(build_preview_mat(
                    window,
                    name,
                    img,
                    preview_font_size
                ))

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

                    popup = build_preview_popup(window, label=name, subtitle='By Miki3DX', image=img)
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
        tag_redraw(context)
        return {'FINISHED'}


class FLUIDP_OT_undraw_material(bpy.types.Operator):
    bl_label = 'undraw_material'
    bl_idname = 'fluidp.undraw_material'

    def execute(self, context: bpy.types.Context):
        for index, handler in enumerate(handlers):
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        handlers.clear()
        EventCatcher.stop()

        tag_redraw(context)

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
