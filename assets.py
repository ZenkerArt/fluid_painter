import os

import bpy
base_path = os.path.realpath(os.path.dirname(__file__))

lib_path = os.path.join(base_path, 'files/FluidLib.blend')


class Assets:
    images: list[bpy.types.Image] = []
    fluid_logo_black: bpy.types.Image

    @classmethod
    def load(cls):
        cls.fluid_logo_black = load_image(r'files\assets\logo\logo_fluid_black.png')
        images = []

        # base_path = os.path.realpath(os.path.dirname(__file__))
        # for i in os.scandir(os.path.join(base_path, './files/Pics')):
        #     images.append(load_image(i.path))

        # cls.images = images


def load_image(ipath: str):
    path = os.path.join(base_path, ipath)
    image = bpy.data.images.load(path, check_existing=True)
    image.gl_load()

    return image
