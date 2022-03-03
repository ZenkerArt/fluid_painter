import os
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Iterable, Any
from ...assets import Assets

import bpy


@dataclass
class MaterialsViewerItem:
    name: str
    image: bpy.types.Image


@dataclass
class MaterialsViewerBlendItem(MaterialsViewerItem):
    path: str

    def load(self):
        name = f'Fluid_{self.name}_Object'
        original_object = bpy.data.objects.get(name)

        if original_object is None:
            lib = bpy.data.libraries.load(self.path)
            with lib as (data_from, data_to):
                data_to.objects.append(name)

            original_object = bpy.data.objects[name]

        new_object = original_object.copy()
        new_object.data = original_object.data.copy()
        return new_object.copy()


class MaterialViewList(ABC, Iterable[MaterialsViewerItem]):
    @abstractmethod
    def get(self, index: int) -> MaterialsViewerItem:
        pass

    @abstractmethod
    def length(self) -> int:
        pass

    def __len__(self):
        return self.length()

    def __getitem__(self, item: int):
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or self.length()

            if stop > self.length():
                stop -= stop - self.length()

            return [self.get(i) for i in range(start, stop)]
        if not isinstance(item, int):
            raise IndexError(f'Index not be {type(item)} only int.')

        return self.get(item)

    def __iter__(self):
        return (self.get(i) for i in range(0, self.length()))


class SceneMaterials(MaterialViewList):
    _materials: list[MaterialsViewerItem]

    def __init__(self):
        self._materials = []

        for i in bpy.data.materials:
            if not i.name.startswith('Fluid'):
                continue

            image_name = i.name.replace(' - ', '_').replace(' ', '') + '.png'
            image = bpy.data.images.get(image_name, Assets.fluid_logo_black)

            self._materials.append(MaterialsViewerItem(
                material=i.name,
                image=image
            ))

    def get(self, index: int) -> MaterialsViewerItem:
        return self._materials[index]

    def length(self) -> int:
        return len(self._materials)


class BlendMaterials(MaterialViewList):
    _materials: list[MaterialsViewerBlendItem]
    _path: str
    _cache: dict[int, MaterialsViewerBlendItem]

    def __init__(self, path: str):
        self._materials = []
        self._path = path
        self._cache = {}

        lib = bpy.data.libraries.load(path)

        with lib as (data_from, data_to):
            for i in data_from.objects:
                _, name, _ = i.split('_')
                image = bpy.data.images.get(f'Fluid_{name}.png', Assets.fluid_logo_black)
                image.gl_load()

                self._materials.append(MaterialsViewerBlendItem(
                    name=name,
                    image=image,
                    path=path
                ))

    def get(self, index: int) -> MaterialsViewerItem:
        result = self._cache.get(index)

        if result is not None:
            return result

        mat = self._materials[index].name

        try:
            self._materials[index].image = bpy.data.images[f'Fluid_{mat}_Image.png']
            self._cache[index] = self._materials[index]
            return self._materials[index]
        except Exception as e:
            pass

        lib = bpy.data.libraries.load(self._path)

        with lib as (data_from, data_to):
            data_to.images.append(f'Fluid_{mat}_Image.png')

        try:
            self._materials[index].image = bpy.data.images[f'Fluid_{mat}_Image.png']
        except Exception as e:
            self._materials[index].image = Assets.fluid_logo_black
            print(e)
        self._cache[index] = self._materials[index]
        return self._materials[index]

    def length(self) -> int:
        return len(self._materials)
