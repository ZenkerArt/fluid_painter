# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
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

reg, unreg, modules = register_package('./modules', 'modules')

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
