import bpy
from .operators import FLUIDP_OT_draw_material, FLUIDP_OT_undraw_material, FLUIDP_OT_scroll


class FLUIDP_PT_materials_viewer(bpy.types.Panel):
    bl_label = 'Material'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fluid Painter'

    def draw(self, context: bpy.types.Context):
        self.layout.operator(FLUIDP_OT_draw_material.bl_idname)
        self.layout.operator(FLUIDP_OT_undraw_material.bl_idname)

        s = self.layout.split()

        s.operator(FLUIDP_OT_scroll.bl_idname, text='<').scroll = -1
        s.operator(FLUIDP_OT_scroll.bl_idname, text='>').scroll = 1


class FLUIDP_PT_materials_viewer_context_menu(bpy.types.Menu):
    bl_label = 'Materials Viewer'
    bl_idname = 'FLUIDP_PT_materials_viewer_context_menu'

    def draw(self, context: bpy.types.Context):
        self.layout.operator(FLUIDP_OT_undraw_material.bl_idname)


classes = [FLUIDP_PT_materials_viewer, FLUIDP_PT_materials_viewer_context_menu]
