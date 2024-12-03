import flet as ft

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.reviuse_cards import reviuse_cards


class div_reviuse(ft.Container):
    def __init__(self,page,rows:int=4,check=0,position=1145):
        self.page=page
        self.my_cards=reviuse_cards(self.page,rows=rows)

        self.back_ref=ft.Ref[ft.OutlinedButton]()
        self.next_ref=ft.Ref[ft.OutlinedButton]()

        self.back_block=False
        self.next_block=False

        self.check=check

        if 0>self.my_cards.position_start-4:
            self.back_block=True
        if self.my_cards.position_last+1>self.my_cards.length_reviews:
            self.next_block=True




        super().__init__(
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        width=500,
                        content=CustomizeText("Відгуки клієнтів", font_family="Playfair Display", size=48),
                    ),
                    ft.Row(
                        width=position,
                        alignment="spaceBetween",
                        controls=[
                            ft.Container(
                                content=ft.OutlinedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.KEYBOARD_ARROW_LEFT_OUTLINED),
                                            CustomizeText(text="Попередні відгуки",size=14),
                                        ],
                                    ),
                                    on_click=lambda e:self.navigate_back(),
                                    ref=self.back_ref,
                                    disabled=self.back_block
                                )
                            ),
                            ft.Container(
                                content=ft.OutlinedButton(
                                    content=ft.Row(
                                        controls=[
                                            CustomizeText(text="Наступні відгуки",size=14),
                                            ft.Icon(name=ft.icons.KEYBOARD_ARROW_RIGHT_OUTLINED)
                                        ]
                                    ),
                                    on_click=lambda e:self.navigate_next(),
                                    ref=self.next_ref,
                                    disabled=self.next_block
                                )
                            ),
                        ],
                    ),
                    self.my_cards,
                ]
            )
        )
        if self.check==0:
            self.contein=ft.Container(
                margin=ft.margin.only(top=5,bottom=10,left=5),
                content=CustomButton(text="Залишити відгук",
                                     height=50,
                                     width=300,
                                     text_size=20,
                                     on_click=lambda event: self.page.go("/add_response")
                                     )
            )
            self.content.controls.append(self.contein)


    def navigate_next(self):
        self.my_cards.go_next()
        self.blocked_navigate()


    def navigate_back(self):
        self.my_cards.go_back()
        self.blocked_navigate()


    def blocked_navigate(self):
        start=self.my_cards.position_start
        finish=self.my_cards.position_last

        if start-4<0:
            self.back_ref.current.disabled=True
        else:
            self.back_ref.current.disabled=False

        if finish+1>self.my_cards.length_reviews:
            self.next_ref.current.disabled=True
        else:
            self.next_ref.current.disabled=False

        self.page.update()
