import bpy


class FLUIDP_OT_curve_physic_generate(bpy.types.Operator):
    def execute(self, context: bpy.types.Context):
        pass


class FLUIDP_PT_curve_physic(bpy.types.Panel):
    bl_label = 'Curve Physic'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fluid Painter'

    def draw(self, context: bpy.types.Context):
        pass


classes = [
    FLUIDP_PT_curve_physic
]
