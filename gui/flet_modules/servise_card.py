import flet as ft
from gui.flet_modules.customize_text import CustomizeText


class servise_card(ft.Card):
    def __init__(self,img_src:str,h1_text:str,paragraph:str,price:str):
        self.img_src = img_src
        self.h1_text = h1_text
        self.paragraph = paragraph
        self.price=price
        super().__init__(
                width=280,
                height=330,
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src=f"{img_src}",
                            width=280,
                            height=180,
                            fit=ft.ImageFit.COVER
                        ),
                        CustomizeText(text=f"{h1_text}", weight="900", size=23,text_align="center"),
                        ft.Container(padding=ft.padding.only(left=5,right=5),
                                     height=50,
                                     content=CustomizeText(
                                         text=f"{paragraph}",
                                         size=12, font_family="Lato", text_align="justify")),
                        ft.Container(
                            padding=ft.padding.only(left=5, right=5),
                            content=CustomizeText(
                                text=f"Ціна від {price} гривень",
                                size=10,
                                font_family="Lato"
                            )
                        )
                    ]
                )
        )