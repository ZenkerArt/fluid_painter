import bpy
from .types import FluidMaterialType
from .models import PropType


class FLUIDP_OT_add_material_prop(bpy.types.Operator):
    bl_label = 'Add Material Prop'
    bl_idname = 'fluidp.add_material_prop'
    mat_name: bpy.props.StringProperty()

    prop_name: bpy.props.StringProperty(default='prop')
    prop_value: bpy.props.FloatProperty(default=1.0)
    prop_type: bpy.props.EnumProperty(items=PropType.generate_enum(), default=PropType.float)

    def execute(self, context: bpy.types.Context):
        material: FluidMaterialType = bpy.data.materials[self.mat_name]
        props = material.fluid_mat.props
        prop = props.add()
        prop.name = self.prop_name
        prop.value = self.prop_value

        return {'FINISHED'}


class FLUIDP_OT_edit_material_prop(bpy.types.Operator):
    bl_label = 'Edit Material Prop'
    bl_idname = 'fluidp.edit_material_prop'

    remove: bpy.props.BoolProperty(options={'HIDDEN'}, default=False)
    mat_name: bpy.props.StringProperty(options={'HIDDEN'})

    prop_index: bpy.props.IntProperty(options={'HIDDEN'})
    type: bpy.props.EnumProperty(
        items=PropType.generate_enum()
    )

    def execute(self, context: bpy.types.Context):
        material: FluidMaterialType = bpy.data.materials[self.mat_name]
        props = material.fluid_mat.props

        if self.remove:
            props.remove(self.prop_index)
            return {'FINISHED'}

        return {'FINISHED'}

    def draw(self, context: 'Context'):
        layout = self.layout

        material: FluidMaterialType = bpy.data.materials[self.mat_name]
        props = material.fluid_mat.props
        prop = props[self.prop_index]

        row = layout.row()
        row.label(text='Name')
        row.prop(prop, 'name', text='')

        row = layout.row()
        row.label(text='Type')
        row.prop(prop, 'type', text='', emboss=False)

    def invoke(self, context: 'bpy.types.Context', event: 'bpy.types.Event'):
        if self.remove:
            return self.execute(context)
        return context.window_manager.invoke_props_dialog(self)


classes = [FLUIDP_OT_add_material_prop, FLUIDP_OT_edit_material_prop]
