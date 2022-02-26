import bpy
from ...types.icons import Icons
from .base_tab import FluidBaseTab


class BubbleLayer(FluidBaseTab):
    def create_bubble_settings(self, inputs: list[int]):
        names = ['Enable', 'Are Inside', 'Size', 'Amount', 'Shift', 'Seed']

        self.create_search_field(inputs[0], bpy.data, 'materials', icon=Icons.material)

        for index, input_index in enumerate(inputs[1:]):
            name = names[index]
            if name == 'Seed':
                self.create_field(input_index, name)
            else:
                self.create_field(input_index, name, slider=True)


class FLUIDP_PT_bubbles(FluidBaseTab, bpy.types.Panel):
    bl_label = 'Bubbles'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        pass


class FLUIDP_PT_bubble_layer_1(BubbleLayer, bpy.types.Panel):
    bl_label = 'Layer 1'
    bl_parent_id = 'FLUIDP_PT_bubbles'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        self.create_bubble_settings([25, 4, 14, 8, 9, 46, 44])


class FLUIDP_PT_bubble_layer_2(BubbleLayer, bpy.types.Panel):
    bl_label = 'Layer 2'
    bl_parent_id = 'FLUIDP_PT_bubbles'

    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        self.create_bubble_settings([26, 16, 17, 24, 23, 47, 45])


classes = [FLUIDP_PT_bubbles, FLUIDP_PT_bubble_layer_1, FLUIDP_PT_bubble_layer_2]
