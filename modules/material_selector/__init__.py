from typing import Any

from .tabs import classes as tabs
from ...reglib import ModuleRegister


class Register(ModuleRegister):
    def register(self) -> list[Any]:
        return tabs
