import flet as ft
from anyio.abc import value

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

        self.default_value="Користувач"

        self.tracker = {
            "user":False,
            "password": False,
        }

        super().__init__(
            alignment=ft.Alignment(0,0),
            modal=True,
            shadow_color=ft.Colors.GREY,
            title=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=self.close_modal,
                    icon_color=ft.Colors.RED
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
                                    ft.Radio(value="Перукар",label="Перукар"),
                                    ft.Radio(value="Користувач",label="Користувач")
                                    ],
                                ),
                                on_change=lambda e:self.get_value_group(),
                                ref=self.radio_ref
                            )
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[ft.TextField(
                            height=60,
                            label="Логін/Email",
                            max_length=25,
                            border_color=ft.Colors.GREY,
                            prefix_icon=ft.icons.CANCEL,
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
                            border_color=ft.Colors.GREY,
                            prefix_icon=ft.icons.CANCEL,
                            border_width=0.5,
                            ref=self.password_ref,
                            on_change=lambda e:self.password_correct()

                        )]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.TextButton(content=ft.Container(CustomizeText(text="Є акаунт",color=ft.Colors.BLUE_ACCENT,size=15),
                                                               border=ft.border.only(
                                                                   bottom=ft.border.BorderSide(1,ft.Colors.BLUE_ACCENT))

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

    def modal_register(self):
        from gui.utils import open_register
        self.close_modal()
        open_register(self.page)

    def give_user(self):
        username=self.loginned(self.user_ref.current.value,self.password_ref.current.value)
        if username=="":
            self.user_ref.current.value=""
            self.password_ref.current.value=""
            self.error_text.current.controls.append(
                CustomizeText(
                    text="Неправильний пароль або логін",
                    size=12,
                    color=ft.Colors.RED,
                )
            )
        else:
            print(username)
            self.page.client_storage.set("user",f"{username}")
            self.close_modal()


    def user_correct(self):
        if len(self.user_ref.current.value)>=3:
            self.tracker["user"] = True
            self.user_ref.current.prefix_icon = ft.icons.CHECK
            self.user_ref.current.error_text = ""
        else:
            self.tracker["user"] = False
            self.user_ref.current.prefix_icon = ft.icons.CANCEL
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
            self.password_ref.current.prefix_icon=ft.icons.CHECK
            self.password_ref.current.error_text=""
        else:
            self.tracker["password"]=False
            self.password_ref.current.prefix_icon=ft.icons.CANCEL
            self.password_ref.current.error_text="Мінімум 8 символів"
        self.check_track()
        self.page.update()


    def get_value_group(self):
        print(self.radio_ref.current.value)
        self.close_modal()


    def close_modal(self, e="None"):
        self.open=False,
        self.page.update()