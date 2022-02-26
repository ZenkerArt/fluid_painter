import bpy
from . import FluidMaterial, FluidPainterMaterialProp
from ...types.bpy_struct import CollectionPropertyType


class FluidMaterialBodyType(FluidMaterial, bpy.types.Material):
    enable: bool
    props: CollectionPropertyType[FluidPainterMaterialProp]


class FluidMaterialType(bpy.types.Material):
    fluid_mat: FluidMaterialBodyType
