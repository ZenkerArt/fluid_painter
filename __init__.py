import logging

import bpy
from .reglib import register_package

bl_info = {
    "name": "Fluid Painter",
    "author": "Zenker, Miki3dx",
    "description": "",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "https://github.com/ZenkerArt/fluid_painter",
    "warning": "",
    "category": "3D View"
}

reg, unreg, modules = register_package('./modules', 'modules', __package__)

classes = [
    *reg,
]

classes_unreg = [
    *unreg
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for mod in modules:
        mod.unregister()

    for cls in [*classes, *classes_unreg]:
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            logging.warning(f'{cls.__name__}: {e.args[0]}')
