import flet as ft

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.reviuse_card import reviuse_card
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.clicked_stars import clicked_stars




class add_response(ft.Column):
    def __init__(self,page,screen_width):
        super().__init__(
            alignment=ft.alignment.center
        )
        self.page=page

        self.container_ref=ft.Ref[ft.Container]()
        self.textfield_ref=ft.Ref[ft.TextField]()
        self.text_ref=ft.Ref[ft.Container]()

        self.adapt=0

        self.star_rate=clicked_stars()
        self.screen_width=screen_width
        self.div_reviuse = ft.Row(
            expand=True,
            alignment="center",
            controls=[
                ft.Container(
                    ref=self.container_ref,
                    width=900,
                    alignment=ft.alignment.top_center,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    CustomizeText("Відгуки клієнтів", font_family="Playfair Display", size=48),
                                ]
                            ),
                            ft.Row(
                                alignment=ft.alignment.center,
                                controls=[
                                    reviuse_card()
                                ],
                            ),
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
                                    max_length=500,
                                    text_size=15,
                                    width="auto",
                                    min_lines=5,
                                    multiline=True,
                                    label="Розкажіть про свої враження",
                                )
                            ),
                            ft.Row(
                                expand=True,
                                alignment="center",
                                controls=[
                                    ft.Container(
                                        content=CustomButton(
                                            text="Опублікувати відгук",
                                            height=50,
                                            width=300,
                                            text_size=19,
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
        self.controls.append(
            self.div_reviuse
        )
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

