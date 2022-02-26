import logging
import os
from abc import ABC
from importlib import import_module
from typing import Any

import bpy
from .config import DISABLE_MODULES


class ClsReg:
    def register(self, cls: Any):
        bpy.utils.register_class(cls)

    def register_list(self, classes: list[Any]):
        for cls in classes:
            self.register(cls)


class ModuleRegister(ABC):
    def raw_register(self, reg: ClsReg):
        pass

    def register(self) -> list[Any]:
        return []

    def unregister(self):
        pass

    def init(self):
        self.raw_register(ClsReg())
        result = self.register()

        if not isinstance(result, list):
            raise ValueError('Required list.')

        return result


def register_package(path: str, module_name: str):
    clss = []

    base_path = os.path.dirname(__file__)

    for i in os.scandir(os.path.join(base_path, path)):
        try:
            if i.name.startswith('_') or i.name.startswith('util') or i.name in DISABLE_MODULES:
                continue
            name: str = i.name

            module = import_module(f'.{module_name}.{name}', 'fluid_painter')

            if not hasattr(module, 'Register'):
                logging.info(f'Module {name} ignored.')
                continue

            logging.info(f'Register module "{name}" from "{module_name}".')
            result: ModuleRegister = module.Register()

            clss.extend(result.init())
        except Exception as e:
            raise type(e)(f'{module_name}.{name}: {e.args[0]}')

    return clss
