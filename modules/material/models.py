import bpy


class PropType:
    float: str = 'float'
    float_vector: str = 'float_vector'
    slider: str = 'slider'

    @staticmethod
    def generate_enum():
        enum = []

        for name, t in PropType.__annotations__.items():
            enum.append(
                (name, name.replace('_', ' ').title(), '')
            )

        return enum


class FluidMaterial(bpy.types.PropertyGroup):
    enable: bpy.props.BoolProperty()


class FluidPainterMaterialProp(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    float: bpy.props.FloatProperty()
    slider: bpy.props.FloatProperty(subtype='FACTOR', min=0, max=1)
    float_vector: bpy.props.FloatVectorProperty()

    type: bpy.props.EnumProperty(
        items=PropType.generate_enum()
    )
