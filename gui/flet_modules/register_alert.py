import flet as ft
import re
import bcrypt


from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.login_alert import login_alert
from db.db_use import db_use

class register_alert(ft.AlertDialog,db_use):
    def __init__(self,page:ft.Page):
        self.page=page

        self.name_ref=ft.Ref[ft.TextField]()
        self.username_ref=ft.Ref[ft.TextField]()
        self.email_ref=ft.Ref[ft.TextField]()
        self.phone_ref=ft.Ref[ft.TextField]()
        self.password_ref=ft.Ref[ft.TextField]()
        self.password_repeat_ref=ft.Ref[ft.TextField]()
        self.register_ref=ft.Ref[ft.ElevatedButton]()

        self.tracker={
            "name":False,
            "login":False,
            "email":False,
            "password":False,
            "password_repeat":False,
        }
        self.tracker["login"]

        super().__init__(
            alignment=ft.Alignment(0,0),
            modal=True,
            shadow_color=ft.Colors.GREY,
            content=ft.Column(
                width=450,
                height=600,
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                content=CustomizeText(text="Реєстрація",size=30,weight="bold")
                            )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Прізвище Ім'я",
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            prefix_icon=ft.icons.CANCEL,
                            ref=self.name_ref,
                            on_change=lambda e:self.name_correct(),
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="email",
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            ref=self.email_ref,
                            on_change=lambda e:self.email_correct(),
                            prefix_icon=ft.icons.CANCEL,
                            on_blur=lambda e:self.email_find(),
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Номер (Не обов'язково)",
                            prefix_text="+380",
                            border_color=ft.Colors.GREY,
                            input_filter=ft.InputFilter(allow=True, regex_string=r"^\+?[0-9]*$", replacement_string=""),
                            border_width=0.5,
                            ref=self.phone_ref,
                            max_length=9,
                            prefix_icon=ft.icons.CHECK,
                            on_change=lambda e: self.email_correct(),
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Логін",
                            max_length=25,
                            border_color=ft.Colors.GREY,
                            keyboard_type=ft.KeyboardType.NAME,
                            border_width=0.5,
                            ref=self.username_ref,
                            prefix_icon=ft.icons.CANCEL,
                            input_filter=ft.InputFilter(allow=True, regex_string=r"^[a-z]+$", replacement_string=""),
                            on_change=lambda e:self.login_correct(),
                            on_blur=lambda e:self.username_find()
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Пароль",
                            password=True,
                            can_reveal_password=True,
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            ref=self.password_ref,
                            prefix_icon=ft.icons.CANCEL,
                            on_change=lambda e:self.password_correct()
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Повторіть пароль",
                            password=True,
                            can_reveal_password=True,
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            ref=self.password_repeat_ref,
                            prefix_icon=ft.icons.CANCEL,
                            on_change=lambda e: self.password_correct()

                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.TextButton(content=ft.Container(CustomizeText(text="Увійти",color=ft.Colors.BLUE_ACCENT,size=15),
                                                               border=ft.border.only(
                                                                   bottom=ft.border.BorderSide(1,ft.Colors.BLUE_ACCENT))

                                                               ),
                                          on_click=self.open_login,
                                          )
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            CustomButton(
                            ref=self.register_ref,
                            text="Зареєструватись",
                            text_size=18,
                            width=200,
                            height=50,
                            on_click=lambda e:self.input_database(),
                        )]
                    )
                ]
            )
        )


    def open_login(self,event):
        self.close_modal()
        self.page.open(login_alert(self.page))
        self.page.update()


    def push_error(self):
        pass


    def input_database(self):
        temp=self.create_row(self.name_ref.current.value,self.username_ref.current.value,self.email_ref.current.value,self.phone_ref.current.value,self.password_ref.current.value)
        if temp==True:
            self.close_modal()
        else:self.push_error()


    def email_correct(self):
        patterns=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3,}$"

        if re.fullmatch(patterns,self.email_ref.current.value):
            self.tracker["email"]=True
            self.email_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.tracker["email"]=False
            self.email_ref.current.prefix_icon=ft.icons.CANCEL
        self.check_track()
        self.page.update()

    def phone_correct(self):
        if len(self.phone_ref.current.value)==9 or len(self.phone_ref.current.value)==0:
            self.phone_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.phone_ref.current.prefix_icon=ft.icons.CANCEL
        self.page.update()

    def password_correct(self):
        if len(self.password_ref.current.value)>=8:
            self.tracker["password"]=True
            self.password_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.tracker["password"]=False
            self.password_ref.current.prefix_icon=ft.icons.CANCEL

        if self.password_ref.current.value == self.password_repeat_ref.current.value and self.tracker["password"]:
            self.tracker["password_repeat"]=True
            self.password_repeat_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.tracker["password_repeat"]=False
            self.password_repeat_ref.current.prefix_icon=ft.icons.CANCEL
        self.check_track()
        self.page.update()


    def disabled_button(self,current=True):
        self.register_ref.current.disabled=current
        self.register_ref.current.update()


    def login_correct(self):
        if len(self.username_ref.current.value)>=3:
            self.tracker["login"]=True
            self.username_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.tracker["login"]=False
            self.username_ref.current.prefix_icon=ft.icons.CANCEL

        self.check_track()
        self.page.update()


    def check_track(self):
        for i in self.tracker.values():
            if i!=True:
                self.disabled_button(current=True)
                return False
        self.disabled_button(current=False)


    def email_find(self):
        if self.check_email(self.email_ref.current.value):
            self.check_track()
            self.email_ref.current.error_text = "Користувач з таким email вже є"
            self.email_ref.current.prefix_icon=ft.icons.CANCEL,
            self.tracker["email"] = False
        else:
            self.check_track()
            self.email_ref.current.error_text=""
            self.tracker["email"] = True
        self.page.update()


    def username_find(self):
        if self.check_name(self.username_ref.current.value):
            self.disabled_button(current=True)
            self.username_ref.current.error_text="Користувач з таким username вже є"
            self.username_ref.current.prefix_icon=ft.icons.CANCEL,
            self.tracker["login"]=True
        else:
            self.check_track()
            self.username_ref.current.error_text=""
            self.tracker["login"] = True
        self.page.update()


    def name_correct(self):
        patterns=r"^[А-ЯІЇЄҐA-Z][а-яіїєґa-z]+ [А-ЯІЇЄҐA-Z][а-яіїєґa-z]+$"

        if re.fullmatch(patterns,self.name_ref.current.value):
            self.tracker["name"]=True
            print(self.tracker)
            self.name_ref.current.prefix_icon=ft.icons.CHECK
        else:
            self.tracker["name"]=False
            self.name_ref.current.prefix_icon=ft.icons.CANCEL


        self.check_track()
        self.page.update()


    def close_modal(self, e=None):
        self.open=False,
        self.page.update()