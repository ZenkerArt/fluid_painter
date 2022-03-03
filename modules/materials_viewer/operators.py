import bpy
from .material_list import BlendMaterials, MaterialsViewerBlendItem
from .ui import build_preview_popup, MaterialsViewer, MaterialsViewerItem
from .utils import get_regions, tag_redraw
from ..fluid_painter.utils import get_geo_modifier
from ...assets import Assets, lib_path
from ...blendui.events import EventCatcher
from ...blendui.layouts import VLayout
from ...blendui.utils import Color
from ...blendui.widgets import Style, Vec2D
from ...blendui.window import Window

handlers = []
materials_viewer = MaterialsViewer()


class ActiveWidget:
    widget: VLayout = VLayout()
    data: MaterialsViewerItem = None

    @classmethod
    def is_hover(cls):
        return cls.widget.events.is_hover()

    @classmethod
    def valid(cls):
        return cls.data is not None and cls.is_hover()


class FLUIDP_OT_create_curve(bpy.types.Operator):
    bl_label = 'Create fluid curve'
    bl_idname = 'fluidp.create_curve'
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context: bpy.types.Context):
        bpy.ops.object.mode_set(mode='OBJECT')
        if isinstance(ActiveWidget.data, MaterialsViewerBlendItem):
            d = ActiveWidget.data
            obj = d.load()
            geo = get_geo_modifier(obj)
            objs = []

            for i in context.selected_objects:
                if i.name.startswith('Fluid'):
                    continue

                objs.append(i)

            if len(objs) == 1 and '+' in d.name:
                geo['Input_41'] = objs[0]

            context.collection.objects.link(obj)
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}

        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '3D'
        spline = crv.splines.new(type='BEZIER')

        obj = bpy.data.objects.new(f'FluidPainterCurve - {self.material_name}', crv)
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
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        region, ui = get_regions(context)
        EventCatcher.event(event)

        if not EventCatcher.is_running:
            EventCatcher.is_running = False
            return {'CANCELLED'}
        tag_redraw(context)
        EventCatcher.mouse_offset = (region.x, region.y)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and ActiveWidget.valid():
            bpy.ops.fluidp.create_curve(material_name=ActiveWidget.data.name)
            return {"RUNNING_MODAL"}

        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS' and ActiveWidget.valid():
            bpy.ops.wm.call_menu(name='FLUIDP_PT_materials_viewer_context_menu')
            return {"RUNNING_MODAL"}

        if event.type == 'WHEELUPMOUSE' and event.value == 'PRESS' and ActiveWidget.valid():
            materials_viewer.scroll -= 1
            return {"RUNNING_MODAL"}

        if event.type == 'WHEELDOWNMOUSE' and event.value == 'PRESS' and ActiveWidget.valid():
            materials_viewer.scroll += 1
            return {"RUNNING_MODAL"}

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class FLUIDP_OT_draw_material(bpy.types.Operator):
    bl_label = 'Open Assets'
    bl_idname = 'fluidp.draw_material'
    options = ['UNDO_GROUPED']

    scroll: bpy.props.IntProperty('Scroll', default=0)

    def execute(self, context: bpy.types.Context):
        Assets.load()
        # materials = SceneMaterials()
        materials = BlendMaterials(lib_path)
        materials_viewer.scroll = 0

        def draw():
            try:
                region, ui = get_regions(context)
                window = Window(region, ui)
                scale = window.scale

                if region != context.region:
                    return

                materials_viewer.materials = materials
                materials_viewer.window = window
                materials_viewer.init()
                layout = materials_viewer.draw()

                popup_offset = 140 * scale
                layouts: list[VLayout] = layout.widgets

                for index, wid in enumerate(layouts):
                    if wid.events.is_hover():
                        fluid_mat = materials_viewer.materials_scroll[index]
                        width = wid.width * 3
                        margin = materials_viewer.margin

                        x = wid.x - margin / 2 + popup_offset / 2
                        y = wid.y + wid.height + margin / 2 + popup_offset / 2 + 20 * scale

                        popup = build_preview_popup(window, label=fluid_mat.name, subtitle='By Miki3DX',
                                                    image=fluid_mat.image)

                        if x + width + popup_offset > window.width:
                            x = x - (x + width + popup_offset / 2 + 20 * scale - window.width)

                        popup.set_width(wid.width * 3)
                        popup.set_pos(x, y)

                        style = Style(popup)
                        style.add_background(
                            size=Vec2D(1),
                            offset=Vec2D(popup_offset),
                            color=Color(.1, .1, .1)
                        )

                        popup.draw()

                        ActiveWidget.widget = wid
                        ActiveWidget.data = fluid_mat
            except Exception as e:
                print(e)
                for index, handler in enumerate(handlers):
                    bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
                handlers.clear()
                EventCatcher.stop()

                tag_redraw(context)

        draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW',
                                                              'POST_PIXEL')
        EventCatcher.run()
        handlers.append(draw_handler)
        tag_redraw(context)
        return {'FINISHED'}


class FLUIDP_OT_undraw_material(bpy.types.Operator):
    bl_label = 'Close Assets'
    bl_idname = 'fluidp.undraw_material'
    options = []

    def execute(self, context: bpy.types.Context):
        for index, handler in enumerate(handlers):
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        handlers.clear()
        EventCatcher.stop()

        tag_redraw(context)

        return {'FINISHED'}


class FLUIDP_OT_scroll(bpy.types.Operator):
    bl_label = 'Scroll'
    bl_idname = 'fluidp.scroll'

    scroll: bpy.props.IntProperty(default=0)

    def execute(self, context: bpy.types.Context):
        materials_viewer.scroll += self.scroll
        return {'FINISHED'}


classes = [FLUIDP_OT_draw_material, FLUIDP_OT_undraw_material, FLUIDP_OT_event_catcher,
           FLUIDP_OT_create_curve, FLUIDP_OT_scroll]
