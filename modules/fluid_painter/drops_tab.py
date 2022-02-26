import bpy
from .base_tab import FluidBaseTab


class FLUIDP_PT_drops(FluidBaseTab, bpy.types.Panel):
    bl_label = 'Drops'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        self.create_field(31, 'Enable', slider=True)

        if self.get_value(31) == 0:
            return

        self.create_field(33, 'Move')
        self.create_field(34, 'Size', slider=True)
        self.create_field(30, 'Length', slider=True)
        self.create_field(35, 'Exponent', slider=True)


classes = [FLUIDP_PT_drops]
