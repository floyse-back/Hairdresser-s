import flet as ft

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.clicked_stars import clicked_stars
from gui.flet_modules.div_reviuse import div_reviuse
from db.db_use import db_use




class add_response(ft.Column,db_use):
    def __init__(self,page,screen_width):
        super().__init__(
            alignment=ft.alignment.center
        )

        self.page=page


        self.container_ref=ft.Ref[ft.Container]()
        self.textfield_ref=ft.Ref[ft.TextField]()
        self.text_ref=ft.Ref[ft.Container]()

        self.adapt=0

        self.user_disabled,self.user_login=self.check_loginned()

        

        self.star_rate=clicked_stars()
        self.screen_width=screen_width
        self.update_reviuse()


    def update_reviuse(self):
        self.reviuse_cards=div_reviuse(self.page,rows=6,check=1,position=860)

        reviuse= ft.Row(
            expand=True,
            alignment="center",
            controls=[
                ft.Container(
                    ref=self.container_ref,
                    width=900,
                    alignment=ft.alignment.top_center,
                    content=ft.Column(
                        controls=[
                            self.reviuse_cards,
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        ref=self.text_ref,
                                        content=CustomizeText(text="Як би ви оцінили якість обслуговування?", size=24)
                                    )
                                ]
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        self.star_rate,
                                    ]
                                )
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=CustomizeText(
                                            text="Поділіться своїм досвідом",
                                            font_family="Playfair Display",
                                            size=24,
                                        ),
                                    )
                                ]
                            ),
                            ft.Container(
                                margin=ft.margin.only(right=5),
                                content=ft.TextField(
                                    ref=self.textfield_ref,
                                    disabled=self.user_disabled,
                                    max_length=500,
                                    text_size=15,
                                    width="auto",
                                    min_lines=5,
                                    multiline=True,
                                    label=self.user_login,
                                    label_style=ft.TextStyle(
                                        size=20,
                                        color=ft.colors.GREY,
                                    ),
                                    on_change=lambda e:self.correct_element(),
                                    on_focus=lambda e:self.on_focused(),
                                    on_blur=lambda e:self.on_blured()
                                )
                            ),
                            ft.Row(
                                expand=True,
                                alignment="center",
                                controls=[
                                    ft.Container(
                                        content=CustomButton(
                                            text="Опублікувати відгук",
                                            disabled=self.user_login,
                                            height=50,
                                            width=300,
                                            text_size=19,
                                            on_click=lambda e: self.add_response()
                                        )
                                    )
                                ]
                            ),
                        ]
                    )
                )
            ]
        )
        self.controls.clear()
        self.controls.append(
            reviuse
        )

        self.page.update()


    def check_loginned(self):
        if not self.page.client_storage.get("user"):
            return [True,"Спершу зареєструйтесь\n\n\n\n\n"]
        else:
            return [False,"Розкажіть про свої враження\n\n\n\n\n"]


    def on_focused(self):
        self.textfield_ref.current.label=f"{self.user_login.replace('\n','')}"
        self.page.update()


    def on_blured(self):
        if self.textfield_ref.current.label=='':
            self.textfield_ref.current.label=f"{self.user_login}"
        else:
            self.textfield_ref.current.label=f"{self.user_login.replace('\n','')}"
        self.page.update()


    def adaptive_width(self,screen_width):
        if screen_width <900:
            self.container_ref.current.width=screen_width-10
            self.text_ref.current.width=screen_width-40
            self.textfield_ref.current.width=screen_width-50
            self.adapt=1
        elif self.adapt==1:
            self.adapt=0
            self.container_ref.current.width=900
            self.text_ref.current.width="auto"
            self.textfield_ref.current.width="auto"

        self.page.update()


    def add_response(self):
        if not self.check_loginned()[0] and len(self.textfield_ref.current.value)>=2:
            user=self.page.client_storage.get("user")
            self.reviews_insert(username=user,review=self.textfield_ref.current.value,stars=self.star_rate.stars)

            self.textfield_ref.current.value=""
            self.star_rate.stars=0
            self.star_rate.render_stars(0)
            self.page.update()

            self.update_reviuse()
        else:
            self.page.go("/add_response")

    def correct_element(self):
        if self.textfield_ref.current.value=="":
            self.textfield_ref.current.label="Розкажіть про свої враження"
        else:
            self.textfield_ref.current.label="Розкажіть про свої враження"


        self.page.update()

