from typing import Any

from .operators import classes as operators
from .panel import classes as panel
from ...reglib import ModuleRegister


class Register(ModuleRegister):
    def register(self) -> list[Any]:
        return [
            *operators,
            *panel
        ]
