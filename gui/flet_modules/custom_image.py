import flet as ft


class custom_image(ft.Image):
    def __init__(self,src,border_radius=15,**kwargs):
        super().__init__(
            src=src,
            border_radius=ft.border_radius.all(value=border_radius),
            **kwargs,
        )