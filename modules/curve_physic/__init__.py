from typing import Any
from ...reglib import ModuleRegister
from .ui import classes as ui


class Register(ModuleRegister):
    def register(self) -> list[Any]:
        return ui

    def unregister(self):
        pass
