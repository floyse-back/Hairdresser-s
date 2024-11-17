import flet as ft
from gui.flet_modules.customize_text import CustomizeText


class CustomButton(ft.FilledButton):
    def __init__(self,text:str,width:int=250,height:int=75,text_size=30,**kwargs):
        super().__init__(
            content=CustomizeText(text,color=ft.Colors.WHITE,size=text_size,text_align="center"),
            bgcolor="#A67C52",
            width=width,
            height=height,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=20)
            ),
            **kwargs
        )