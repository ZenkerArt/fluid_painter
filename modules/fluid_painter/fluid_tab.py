import bpy
from ...types.icons import Icons
from .base_tab import FluidBaseTab


class FLUIDP_PT_fluid_settings(FluidBaseTab, bpy.types.Panel):
    bl_label = 'Fluid'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        self.create_search_field(3, bpy.data, 'materials', icon=Icons.material)

        self.create_field(27, 'Subdivision', slider=True)
        self.create_field(2, 'Thickness', slider=True)
        self.create_field(13, 'Roughness', slider=True)
        self.create_field(42, 'Adaptivity', slider=True)


class FLUIDP_PT_drawing_settings(FluidBaseTab, bpy.types.Panel):
    bl_label = 'Drawing Settings'
    bl_parent_id = 'FLUIDP_PT_fluid_settings'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        self.create_search_field(41, bpy.data, 'objects', icon=Icons.object_data)
        self.create_search_field(36, bpy.data, 'collections', icon=Icons.outliner_collection)

        if self.get_value(41) is None and self.get_value(36) is None:
            return

        self.create_field(37, 'Flatness', slider=True)
        self.create_field(38, 'Offset')
        self.create_field(40, 'Fading', slider=True)


classes = [FLUIDP_PT_fluid_settings, FLUIDP_PT_drawing_settings]
