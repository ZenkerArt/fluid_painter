from typing import Optional

import bpy
from .operators import FLUIDP_OT_edit_material_prop, FLUIDP_OT_add_material_prop
from .types import FluidMaterialType
from ..fluid_painter.base_tab import FluidBase
from ..fluid_painter.utils import get_geo_modifier


def get_fluid_material(index: int, obj: bpy.types.Object) -> Optional[FluidMaterialType]:
    node = get_geo_modifier(obj)

    if not node:
        return

    return node.get(f'Input_{index}')


class FLUIDP_PT_material_settings(FluidBase, bpy.types.Panel):
    bl_label = 'Material Settings'
    bl_parent_id = 'FLUIDP_PT_fluid_settings'

    @classmethod
    def poll(cls, context: bpy.types.Context):
        mat = get_fluid_material(3, context.active_object)

        return mat is not None and mat.fluid_mat.enable

    def draw(self, context: bpy.types.Context):
        mat = get_fluid_material(3, context.active_object)
        fluid_mat = mat.fluid_mat
        layout = self.layout

        if not fluid_mat.enable:
            return

        properties = fluid_mat.props

        for name, value in properties.items():
            layout.prop(value, value.type, text=name)


class FLUIDP_PT_prop_material_settings(bpy.types.Panel):
    bl_label = "Fluid Painter"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Options"

    def draw(self, context: 'bpy.types.Context'):
        layout = self.layout
        active_material: FluidMaterialType = context.active_object.active_material
        fluid_mat = active_material.fluid_mat
        properties = fluid_mat.props

        layout.prop(fluid_mat, 'enable', text='Enable')

        if not fluid_mat.enable:
            return

        for index, item in enumerate(properties.items()):
            name, value = item

            s = layout.row()
            op = s.operator(FLUIDP_OT_edit_material_prop.bl_idname,
                            text="", icon='PREFERENCES', emboss=False)
            op.mat_name = active_material.name
            op.prop_index = index
            op.remove = False

            # if PropType.color:
            s.prop(value, value.type, text=name)

            re = s.operator(FLUIDP_OT_edit_material_prop.bl_idname,
                            text="", icon='X', emboss=False)
            re.remove = True
            re.mat_name = active_material.name
            re.prop_index = index

        op = layout.operator(FLUIDP_OT_add_material_prop.bl_idname)
        op.mat_name = active_material.name
        op.prop_name = 'prop'
        op.prop_value = 1


classes = [FLUIDP_PT_material_settings, FLUIDP_PT_prop_material_settings]
