from typing import Any

import bpy
from .models import FluidMaterial, FluidPainterMaterialProp
from .operators import classes as operators
from .tab import classes as tab
from ...reglib import ModuleRegister, ClsReg


class Register(ModuleRegister):
    def raw_register(self, reg: ClsReg):
        reg.register_list([
            FluidMaterial,
            FluidPainterMaterialProp
        ])

        FluidMaterial.props = bpy.props.CollectionProperty(type=FluidPainterMaterialProp)

        bpy.types.Material.fluid_mat = bpy.props.PointerProperty(type=FluidMaterial)

    def register(self) -> list[Any]:
        return [
            *operators,
            *tab
        ]
