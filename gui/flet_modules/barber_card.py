import flet as ft

from gui.flet_modules.customize_text import CustomizeText
from db.db_use import db_use

from gui.settings.settings import week_days


class barber_card(ft.Card,db_use):
    def __init__(self,username,img="../gui/static/barbers/den.jpg",name="Валерій Олексійович",text_barber='Сьогодні я зроблю вам свято',position="Перукар з 10 річним досвідом",width=280,height=300):
        self.img=img.replace('../gui/static','')
        self.column_ref=ft.Ref[ft.Column]()
        self.username=username

        self.no_correct=['',None]

        super().__init__(
            width=width,
            height=height,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                margin=ft.margin.only(top=4,left=5),
                                content=ft.CircleAvatar(
                                background_image_src=f"{self.img}",
                                width=50,
                                height=50
                            )
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        width=200,
                                        margin=ft.margin.only(top=4),
                                        content=CustomizeText(text=f"{name}",size=17),
                                    ),
                                    ft.Container(
                                        width=200,
                                        content=CustomizeText(text=f"{position}", size=13, color=ft.colors.GREY)
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        width=250,
                        alignment="center",
                        controls=[
                            CustomizeText(
                                text=f"{text_barber}",
                                size=16,
                            )
                        ]
                    ),
                    ft.Column(
                        ref=self.column_ref,
                        controls=[
                        ]
                    )
                ]
            )
        )
        self.column_ref.current.controls=self.create_rows()


    def create_row(self,day,time):
        return ft.Row(
            width=250,
            alignment="center",
            controls=[
                ft.Container(
                    width=50,
                   content=ft.Icon(
                        name=ft.icons.PUNCH_CLOCK,
                        color=ft.colors.GREY,
                        size=22,
                    )
                ),
                ft.Container(
                    width=200,
                    content=CustomizeText(
                        text=f"{day} {time}",
                        size=18,
                    )
                )
            ]
        )



    def create_rows(self):
        data=self.select_from(name='barberstimetable',timetable=self.username)[0]
        
        new_rows=[]


        if data !=None:
            if data['monday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Понеділок", time=week_days["0"][data['monday']]))
            if data['tuesday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Вівторок", time=week_days["1"][data['tuesday']]))
            if data['wednesday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Середа", time=week_days["2"][data['wednesday']]))
            if data['thursday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Четвер", time=week_days["3"][data['thursday']]))
            if data['friday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Пʼятниця", time=week_days["4"][data['friday']]))
            if data['saturday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Субота", time=week_days["5"][data['saturday']]))
            if data['sunday'] not in self.no_correct:
                new_rows.append(self.create_row(day="Неділя", time=week_days["6"][data['sunday']]))
            return new_rows


