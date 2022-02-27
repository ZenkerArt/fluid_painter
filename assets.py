import os

import bpy


def get_pics() -> list[bpy.types.Image]:
    images = []

    base_path = os.path.realpath(os.path.dirname(__file__))
    for i in os.scandir(os.path.join(base_path, './files/Pics')):
        images.append(load_image(i.path))

    return images


def load_image(ipath: str):
    base_path = os.path.realpath(os.path.dirname(__file__))
    path = os.path.join(base_path, ipath)
    image = bpy.data.images.load(path, check_existing=True)
    image.gl_load()

    return image


def load():
    logo_white = load_image(r'files\assets\logo\logo_fluid_white.png')
    logo_1 = load_image(r'files\assets\logo\logo_fluid_1.png')
    return logo_1, logo_white
