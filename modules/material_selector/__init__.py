from typing import Any

import bpy.types
from ...reglib import ModuleRegister, ClsReg
from .tabs import classes as tabs, MaterialDrawSettings


class Register(ModuleRegister):
    def raw_register(self, reg: ClsReg):
        reg.register(MaterialDrawSettings)

        bpy.types.Scene.fluidp_mat_settings = bpy.props.PointerProperty(type=MaterialDrawSettings)

    def register(self) -> list[Any]:
        return tabs
