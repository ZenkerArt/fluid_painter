from abc import ABC
from typing import Generic, TypeVar

import bpy.types

T = TypeVar('T')


class BpyStructType(Generic[T], bpy.types.bpy_struct, ABC):
    def __getitem__(self, item) -> T:
        pass

    def get(self, key: str, default=None) -> T:
        pass

    def values(self) -> list[T]:
        pass


class CollectionPropertyType(BpyStructType[T]):
    def add(self) -> T:
        pass

    def remove(self, index: int):
        pass
