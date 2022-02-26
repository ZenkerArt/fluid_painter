from abc import abstractmethod
from typing import Any

import bpy
from bpy.types import NodesModifier, UILayout, AnyType
from .utils import has_geo_modifier, get_geo_modifier
from ...types.icons import Icons


class FluidBase:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fluid Painter'


class FluidBaseTab(FluidBase):
    geo_modifier: NodesModifier
    layout: UILayout

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return has_geo_modifier(context.active_object)

    def draw(self, context: 'bpy.types.Context'):
        geo_modifier = get_geo_modifier(context.active_object)
        self.geo_modifier = geo_modifier
        self.draw_tab(geo_modifier)

    def get_value(self, index: int) -> Any:
        return self.geo_modifier.get(f'Input_{index}')

    def create_field(self, index: int, text: str, layout: UILayout = None,
                     **kwargs):
        lay = layout or self.layout
        lay.prop(self.geo_modifier, f'["Input_{index}"]', text=text, **kwargs)

    def create_search_field(self,
                            index: int,
                            search_data: AnyType,
                            prop: str,
                            text: str = '',
                            icon: str = Icons.none,
                            layout: UILayout = None
                            ):
        lay = layout or self.layout

        inputt = f'["Input_{index}"]'
        lay.prop_search(self.geo_modifier, inputt, search_data, prop, text=text, icon=icon)

    @abstractmethod
    def draw_tab(self, geo_mod: bpy.types.NodesModifier):
        pass
