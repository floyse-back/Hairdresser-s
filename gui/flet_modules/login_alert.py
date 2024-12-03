import flet as ft
import time

from db.db_use import db_use
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.customize_text import CustomizeText


class login_alert(ft.AlertDialog,db_use):
    def __init__(self,page:ft.Page):
        self.page=page

        self.user_ref=ft.Ref[ft.TextField]()
        self.password_ref=ft.Ref[ft.TextField]()
        self.radio_ref=ft.Ref[ft.RadioGroup]()
        self.button_ref=ft.Ref[ft.ElevatedButton]()
        self.error_text=ft.Ref[ft.Row]()

        self.default_value="user"

        self.tracker = {
            "user":False,
            "password": False,
        }

        super().__init__(
            alignment=ft.Alignment(0,0),
            modal=True,
            shadow_color=ft.colors.GREY,
            title=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=self.close_modal,
                    icon_color="#A67C52"
                )
                ]
            ),
            content=ft.Column(
                width=450,
                height=400,
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[CustomizeText(text="Увійти",size=30,weight="bold")]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.RadioGroup(
                                content=ft.Row(
                                    alignment="center",
                                    wrap=True,
                                    controls=[
                                    ft.Radio(value="barber",label="Перукар"),
                                    ft.Radio(value="user",label="Користувач")
                                    ],
                                ),
                                ref=self.radio_ref
                            )
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Логін/Email",
                            border_color=ft.colors.GREY,
                            suffix_icon=ft.icons.CLOSE,
                            border_width=0.5,
                            ref=self.user_ref,
                            on_change=lambda e: self.user_correct()
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Пароль",
                            password=True,
                            can_reveal_password=True,
                            border_color=ft.colors.GREY,
                            suffix_icon=ft.icons.CLOSE,
                            border_width=0.5,
                            ref=self.password_ref,
                            on_change=lambda e:self.password_correct()

                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.TextButton(content=ft.Container(CustomizeText(text="Немає акаунта",color=ft.colors.BLUE_ACCENT,size=15),
                                                               border=ft.border.only(
                                                                   bottom=ft.border.BorderSide(1,ft.colors.BLUE_ACCENT))

                                                               ),
                                          on_click=lambda e:self.modal_register(),
                                          )
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[CustomButton(
                            text="Увійти",
                            text_size=18,
                            width=200,
                            height=50,
                            disabled=True,
                            ref=self.button_ref,
                            on_click=lambda e:self.give_user()
                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        ref=self.error_text,
                    )
                ]
            )
        )
        self.radio_ref.current.value="user"


    def modal_register(self):
        from gui.utils import open_register
        self.close_modal()
        open_register(self.page)


    def give_user(self):
        
        if self.radio_ref.current.value==None:
            self.radio_ref.current.value=self.default_value
            
        username=self.loginned(self.user_ref.current.value,self.password_ref.current.value,self.radio_ref.current.value)
        if username=="":
            self.user_ref.current.value=""
            self.password_ref.current.value=""
            self.error_text.current.controls.clear()
            self.error_text.current.controls.append(
                CustomizeText(
                    text="Неправильний пароль або логін",
                    size=12,
                    color=ft.colors.RED,
                )
            )
        else:
            self.page.client_storage.set(key="user",value=username)
            self.page.client_storage.set(key="panel",value=self.radio_ref.current.value)
            time.sleep(0.1)
            self.page.update()
            self.close_modal()
            last_pos=self.page.route
            self.page.snack_bar = ft.SnackBar(
                duration=2000,
                content=ft.Row(
                    alignment="center",
                    controls=[CustomizeText("Ви успішно увійшли",
                                            size=20,
                                            weight="700",
                                            color=ft.colors.WHITE,
                                            )
                              ]
                )
            )
            self.page.snack_bar.open=True
            self.page.go("/reload")
            self.page.go(last_pos)

        self.page.update()


    def user_correct(self):
        if len(self.user_ref.current.value)>=3:
            self.tracker["user"] = True
            self.user_ref.current.suffix_icon = ft.icons.CHECK
            self.user_ref.current.error_text = ""
        else:
            self.tracker["user"] = False
            self.user_ref.current.suffix_icon = ft.icons.CLOSE
            self.user_ref.current.error_text = "Мінімум 3 символа"

        self.check_track()
        self.page.update()


    def disabled_button(self,current=True):
        self.button_ref.current.disabled=current
        self.button_ref.current.update()


    def check_track(self):
        for i in self.tracker.values():
            if i!=True:
                self.disabled_button(current=True)
                return False
        self.disabled_button(current=False)


    def password_correct(self):
        if len(self.password_ref.current.value)>=8:
            self.tracker["password"]=True
            self.password_ref.current.suffix_icon=ft.icons.CHECK
            self.password_ref.current.error_text=""
        else:
            self.tracker["password"]=False
            self.password_ref.current.suffix_icon=ft.icons.CLOSE
            self.password_ref.current.error_text="Мінімум 8 символів"
        self.check_track()
        self.page.update()


    def close_modal(self, e="None"):
        self.open=False,
        self.page.update()