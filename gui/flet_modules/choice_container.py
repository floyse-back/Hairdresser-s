import flet as ft

from gui.flet_modules.customize_text import CustomizeText




class choice_container(ft.Container):
    def __init__(self,text):
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        size=20,
                        color="#A67C52",
                        name=ft.icons.CHECK_CIRCLE,
                    ),
                    ft.Container(
                        width=400,
                        content=CustomizeText(
                        text=text,
                        size=17,
                        text_align="justify",
                    )
                    )
                ]
            ),
            margin=ft.margin.only(right=2,bottom=15),
            width=500,
            height="auto",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "black")),
        )
