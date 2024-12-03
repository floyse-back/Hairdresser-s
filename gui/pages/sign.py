from tkinter import Image

import flet as ft
import re
from flet_core import ButtonStyle, ImageFit

from db.db_use import db_use

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custom_date import custom_date
from gui.flet_modules.div_barbers import div_barbers
from gui.flet_modules.multi_click import multi_click
from gui.flet_modules.barber_column import barber_column

class sign(ft.Column,db_use):
    def __init__(self,page,screen_width):
        super().__init__()
        self.page=page
        self.screen_width=screen_width

        self.phone_ref=ft.Ref[ft.TextField]()
        self.name_ref=ft.Ref[ft.TextField]()
        self.date_ref=ft.Ref[ft.TextField]()

        self.textfield_last=None


        self.tracker={
            "name":False,
            "phone":False,
            "date":False,
            'services':False,
        }
        self.user_info={
            'name':'',
            'phone':'',
            'date_start':'',
        }


        self.last_tracker=False

        self.register_user()

        self.div_text=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=1150,
                    content=CustomizeText("Записатися",weight="bold",size=36),
                )
            ]
        )

        self.price_ref=ft.Ref[ft.Row]()

        self.price_list=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ref=self.price_ref,
            controls=[
                ft.Container(
                    content=CustomizeText(
                        text="Загальна ціна:0",
                    )
                ),
                ft.Container(
                    content=CustomizeText(
                        text="Загальний час: 0"
                    )
                )

            ]
        )

        self.multi_clicked=multi_click(self.page,self.price_ref,func=lambda:self.check_track())


        self.div_info = ft.Container(
            alignment=ft.alignment.center,  # Вирівнювання контейнера в центр
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,  # Центрування елементів у рядку
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            width=500,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.TextField(label="Прізвище та ім'я",
                                             on_change=lambda e: self.correct_name(),
                                             ref=self.name_ref,
                                             helper_text="Введіть прізвище та ім'я"
                                             ),
                                ft.TextField(ref=self.phone_ref,
                                             label="Номер телефону",
                                             helper_text="Номер повинен містити 9 символів",
                                             prefix_text="+380",
                                             input_filter=ft.InputFilter(allow=True, regex_string=r"^\+?[0-9]*$",
                                                                         replacement_string=""),
                                             max_length=9,
                                             on_change=lambda e: self.correct_phone()
                                             ),
                                ft.Stack(controls=[
                                    ft.TextField(label="Дата",ref=self.date_ref,disabled=True,helper_text="Оберіть дату"),
                                    ft.Container(content=ft.TextButton(
                                        icon=ft.icons.CALENDAR_MONTH,
                                        height=55,
                                        width=50,
                                        style=ButtonStyle(
                                            padding=ft.Padding(4,0,0,0),
                                            shape={
                                                ft.MaterialState.DEFAULT:ft.RoundedRectangleBorder(radius=1)
                                            }
                                        ),
                                        on_click=lambda e:page.open(self.custom_dater)
                                    ),
                                    right=0,
                                   )
                                ]),
                                self.multi_clicked,
                            ],
                        ),
                    ),
                    ft.Container(
                        width=650,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="/image/my_sign.jpg",
                            border_radius=5,
                            fit=ImageFit.COVER,
                            width=600,
                            height=500,
                        ),
                    ),
                ],
            ),
        )

        self.custom_dater=custom_date(page=self.page,ref_element=self.date_ref,func=lambda:self.delete_row())

        self.barbers_text=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=1150,
                    content=CustomizeText("Обрати перукаря",weight="bold",size=24),
                ),
            ]
        )

        self.barbers_cards=ft.Column(
            key="reviews",
            width=self.page.width,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment="center",
            controls=[div_barbers(page=self.page)]
        )

        self.sign_ref=ft.Ref[ft.ElevatedButton]()


        self.div_controls=ft.Column(
            controls=[
                self.div_text,
                self.div_info,
                self.barbers_text,
                self.barbers_cards,
            ]
        )

        self.controls.append(
            self.div_controls
        )

        if self.page.client_storage.get('panel')=="user" and self.page.client_storage.get('user') not in ['',None]:
            data=self.select_from('users',username=self.page.client_storage.get('user'))[0]

            self.name_ref.current.value=data['name']
            self.tracker['name']=True
            self.phone_ref.current.value=data['phone'] if data['phone']!=None else ''
            if data['phone']!=None:
                self.tracker['phone']=True


    def check_track(self):
        if len(self.multi_clicked.textfield_ref.current.value)!=0:
            
            if self.textfield_last!=None and self.textfield_last!=self.multi_clicked.textfield_ref.current.value:
                self.last_tracker=not self.last_tracker
                
            self.textfield_last=self.multi_clicked.textfield_ref.current.value
            self.tracker['services']=True
            self.multi_clicked.textfield_ref.current.helper_text=""
        else:
            self.tracker['services']=False
            self.multi_clicked.textfield_ref.current.helper_text="Помилка"

        

        if self.date_ref.current.value!='':
            self.tracker['date']=True
            self.date_ref.current.helper_text=''
        else:
            self.tracker['date'] = False
            self.date_ref.current.helper_text = 'Виберіть дату'

        

        for i in self.tracker.values():
            if i!=True:
                if self.last_tracker!=False:
                    self.last_tracker=False
                    self.delete_row(test=0)
                return False

        if self.last_tracker!=True:
            self.last_tracker=True
            self.delete_row(test=0)
        return True

    def disabled_button(self,current):
        pass


    def correct_name(self):
        patterns = r"^[А-ЯІЇЄҐA-Z][а-яіїєґa-z]+ [А-ЯІЇЄҐA-Z][а-яіїєґa-z]+$"

        if re.fullmatch(patterns, self.name_ref.current.value):
            self.tracker["name"] = True
            self.name_ref.current.helper_text=''
        else:
            self.tracker["name"] = False
            self.name_ref.current.helper_text="Введіть коректне ім'я"

        self.check_track()


    def correct_phone(self):
        if len(self.phone_ref.current.value)==9:
            self.tracker["phone"] = True
            self.phone_ref.current.helper_text=''
        else:
            self.tracker["phone"] = False
            self.phone_ref.current.helper_text='Телефон має мати 9 символів'

        self.check_track()
        self.page.update()


    def register_user(self):
        user=self.page.client_storage.get('user')
        if user !=None and user!='':
            data=self.select_name(f'{user}')
        else:
            data="Користувач не зареєстрований"
        


    def give_time(self):
        return self.multi_clicked.time


    def adaptive_width(self,width):
        pass


    def delete_row(self, test=1):
        if self.last_tracker:
            column=barber_column(page=self.page,date=self.date_ref.current.value,
                                 price=self.multi_clicked.price,
                                 name=self.name_ref.current.value,
                                 phone=self.phone_ref.current.value,
                                 services=" ".join(self.multi_clicked.h1_text),
                                 length=self.multi_clicked.radio_ref.current.value,
                                 time_func=lambda:self.give_time()
                                 )
            self.controls[0].controls[3]=column
        elif not self.last_tracker and test==0:
            
            self.barbers_cards=ft.Column(
            key="reviews",
            width=self.page.width,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment="center",
            controls=[div_barbers(page=self.page)]
        )
            self.controls[0].controls[3]=self.barbers_cards

        self.page.update()