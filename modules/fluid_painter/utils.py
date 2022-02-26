from typing import Optional

import bpy
from ...config import GEO_PREFIX


def get_geo_modifier(obj: bpy.types.Object) -> Optional[bpy.types.NodesModifier]:
    if obj is None:
        return
    
    if not obj.modifiers:
        return

    if len(obj.modifiers) < 0:
        return

    for i in obj.modifiers:
        if hasattr(i, 'node_group') and i.node_group.name.startswith(GEO_PREFIX):
            return i


def has_geo_modifier(obj: bpy.types.Object):
    return get_geo_modifier(obj) is not None
