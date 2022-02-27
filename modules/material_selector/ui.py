import bpy
from ...blendui.window import Window
from ...blendui.widgets import Text, Image
from ...blendui.layouts import VLayout


def build_preview_mat(
        window: Window,
        label: str,
        image: bpy.types.Image,
        label_size: float
):
    scale = window.scale

    p = VLayout()
    p.set_margin(-scale * 50)

    preview_mat = VLayout()
    preview_mat.set_margin(scale * 50)
    preview_mat.add_widget(Text()
                           .set_text(label)
                           .set_height(label_size)
                           .set_color(.8, .8, .8))
    preview_mat.add_widget(Image(image))

    p.add_widget(preview_mat)

    return p


def build_preview_popup(
        window: Window,
        label: str,
        subtitle: str,
        image: bpy.types.Image
):
    scale = window.scale

    preview_mat = VLayout()

    texts = VLayout()
    texts.set_margin(scale * 40)
    texts.add_widget(
        Text()
            .set_text(subtitle)
            .set_height(scale * 25)
            .set_color(255, 255, 255)
            .set_alpha(.5))
    texts.add_widget(
        Text()
            .set_text(label)
            .set_height(scale * 35)
            .set_color(1, 1, 1)
    )

    preview_mat.add_widget(texts)
    preview_mat.add_widget(Image(image))

    preview_mat.set_width(scale * 400)

    return preview_mat
