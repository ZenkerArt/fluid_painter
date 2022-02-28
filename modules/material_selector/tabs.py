import ctypes
from dataclasses import dataclass

import bpy
from .ui import build_preview_mat, build_preview_popup
from .utils import get_regions, tag_redraw
from ...assets import load, get_pics
from ...blendui.events import EventCatcher
from ...blendui.layouts import VLayout, HLayout
from ...blendui.widgets import Text, Image, Rect
from ...blendui.window import Window

handlers = []


@dataclass
class FluidMaterialData:
    material: bpy.types.Material
    image: bpy.types.Image


class ActiveWidget:
    widget: VLayout = VLayout()
    data: FluidMaterialData = None

    @classmethod
    def is_hover(cls):
        return cls.widget.events.is_hover()

    @classmethod
    def valid(cls):
        return cls.data is not None and cls.is_hover()


class MaterialDrawSettings(bpy.types.PropertyGroup):
    row_count: bpy.props.IntProperty(default=5)


class FLUIDP_OT_create_curve(bpy.types.Operator):
    bl_label = 'Create fluid curve'
    bl_idname = 'fluidp.create_curve'
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context: bpy.types.Context):
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '3D'
        spline = crv.splines.new(type='BEZIER')

        obj = bpy.data.objects.new('FluidPainterCurve', crv)
        mod: bpy.types.NodesModifier = obj.modifiers.new(name='Fluid Painter', type='NODES')
        mod.node_group = bpy.data.node_groups['Fluid Painter']
        mod['Input_3'] = bpy.data.materials[self.material_name]
        context.collection.objects.link(obj)

        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


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

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and ActiveWidget.valid():
            bpy.ops.fluidp.create_curve(material_name=ActiveWidget.data.material.name)
            return {"RUNNING_MODAL"}

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
        materials = []

        for i in bpy.data.materials:
            if not i.name.startswith('Fluid'):
                continue

            materials.append(FluidMaterialData(
                material=i,
                image=images[0]
            ))

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

            for fluid_mat in materials[:items_count]:
                name = ' '.join(fluid_mat.material.name)
                layout.add_widget(build_preview_mat(
                    window,
                    name,
                    fluid_mat.image,
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
                    .set_pos(wid.x - bg_size / 2, (wid.y) - bg_size / 2) \
                    .set_size(wid.width + bg_size, wid.width + bg_size) \
                    .draw()
            layout.draw()

            popup_offset = 140 * scale

            layouts: list[VLayout] = layout.widgets
            for index, wid in enumerate(layouts):
                if wid.events.is_hover():
                    fluid_mat = materials[index]
                    width = wid.width * 3
                    x = wid.x - offset / 2 + popup_offset / 2
                    y = wid.y + wid.height + offset / 2 + popup_offset / 2 + 20 * scale

                    popup = build_preview_popup(window, label=fluid_mat.material.name, subtitle='By Miki3DX',
                                                image=fluid_mat.image)

                    if x + width + popup_offset > window.width:
                        x = x - (x + width + popup_offset / 2 + 20 * scale - window.width)

                    popup.set_width(wid.width * 3)
                    popup.set_pos(x, y)
                    popup.compute()

                    Rect() \
                        .set_pos(popup.x, popup.y) \
                        .set_size(popup.width, popup.height) \
                        .set_offset(popup_offset, popup_offset) \
                        .set_color(.1, .1, .1) \
                        .draw()

                    popup.draw()

                    ActiveWidget.widget = wid
                    ActiveWidget.data = fluid_mat

            EventCatcher.reset()

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


classes = [FLUIDP_OT_draw_material, FLUIDP_OT_undraw_material, FLUIDP_PT_material_selector, FLUIDP_OT_event_catcher,
           FLUIDP_OT_create_curve]
