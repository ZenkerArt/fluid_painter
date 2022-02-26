from typing import Any

from ...reglib import ModuleRegister
from .drops_tab import classes as drops_tab
from .bubbles_tab import classes as bubbles_tab
from .fluid_tab import classes as fluid_tab


class Register(ModuleRegister):
    def register(self) -> list[Any]:
        return [
            *fluid_tab,
            *drops_tab,
            *bubbles_tab
        ]
