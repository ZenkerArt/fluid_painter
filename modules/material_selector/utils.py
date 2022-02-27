from typing import Optional

import bpy


def get_region(context: bpy.types.Context, region_name: str, area_name: str = 'VIEW_3D') -> Optional[bpy.types.Region]:
    for area in context.screen.areas:
        if area.type != area_name:
            continue

        for region in area.regions:
            if region.type == region_name:
                return region
    return None


def get_regions(context: bpy.types.Context):
    return get_region(context, 'WINDOW'), get_region(context, 'UI')


def tag_redraw(context: bpy.types.Context):
    window, ui = get_regions(context)
    window.tag_redraw()

    # for area in bpy.context.window.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         area.tag_redraw()
