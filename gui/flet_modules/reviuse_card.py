import flet as ft
import datetime

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.stars_icons import stars_icons


class reviuse_card(ft.Card):
    def __init__(self,text="",stars=1,size_stars=28,username="user",date=datetime.date(2024,11,13),width:int=380,height:int=380):
        super().__init__(
            width=width,
            height=height,
            content=ft.Container(
                padding=ft.padding.all(value=15),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name=ft.icons.ACCOUNT_CIRCLE,
                                    color=ft.colors.BLACK,
                                    size=96,
                                ),
                                ft.Container(
                                    content=ft.Column(controls=[
                                        stars_icons(size_stars=size_stars,stars=stars),
                                        ft.Container(
                                            margin=ft.margin.only(bottom=0),
                                            content=CustomizeText(
                                                text=f"{username}",
                                                size=20,
                                            )
                                        ),
                                        ft.Container(
                                            margin=ft.margin.only(bottom=10),
                                            content=CustomizeText(
                                                text=f"{date}".replace("-","."),
                                                size=12
                                            )
                                        )
                                        ]
                                    )
                                )
                            ]
                        ),
                        ft.Container(
                            margin=ft.margin.only(top=20),
                            content=CustomizeText(
                                text=text,
                                size=14,
                            )
                        )
                    ]
                )
            )
        )
