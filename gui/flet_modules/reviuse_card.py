
import flet as ft
import datetime

from db.db_use import db_use
from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.stars_icons import stars_icons


class reviuse_card(ft.Card):
    def __init__(self,text="",stars=1,size_stars=20,name='testname',username="user",date=datetime.date(2024,11,13),width:int=280,height:int=300):
        self.img=db_use().get_img(user=f"{name}")
        super().__init__(
            width=width,
            height=height,
            content=ft.Container(
                padding=ft.padding.all(value=15),
                content=ft.Column(
                    scroll="auto",
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Image(
                                    src=f"{self.img}".replace('/static/',"/"),
                                    border_radius=10,
                                ),
                                ft.Container(
                                    content=ft.Column(controls=[
                                        stars_icons(size_stars=size_stars,stars=stars),
                                        ft.Container(
                                            width=190,
                                            margin=ft.margin.only(bottom=0),
                                            content=CustomizeText(
                                                text=f"{username}",
                                                size=17,
                                            )
                                        ),
                                        ft.Container(
                                            margin=ft.margin.only(bottom=4),
                                            content=CustomizeText(
                                                text=f"{date}".replace("-","."),
                                                size=11
                                            )
                                        )
                                        ]
                                    )
                                )
                            ]
                        ),
                        ft.Container(
                            margin=ft.margin.only(top=2),
                            width=250,
                            content=CustomizeText(
                                text=text,
                                size=14,
                            )
                        )
                    ]
                )
            )
        )

