import flet as ft


class CustomizeText(ft.Text):
    def __init__(self, text,color="#333333",font_family="Roboto",weight="700",size=20,text_align="justify"):
        super().__init__(
            value=text,
            color=color,
            weight=weight,
            size=size,
            font_family=font_family,
            text_align=text_align
        )

