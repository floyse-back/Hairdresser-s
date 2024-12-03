import flet as ft

from db.db_use import db_use
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.customize_text import CustomizeText


class sign_alert(ft.AlertDialog,db_use):
    def __init__(self,page,user):
        self.page=page
        
        self.my_user=user
        
        super().__init__(
            modal=True,
        )


        
        self.my_column=ft.Column(
            width=600,
            scroll=True,
            controls=self.new_rows()
        )

        self.content=self.my_column


    def new_rows(self):
        self.data=self.select_usersign(username=self.my_user)
        
        
        new_list=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        on_click=lambda e: self.close_modal(),
                        icon_color="#A67C52"
                    )
                ]
            ),
            ft.Row(
                controls=[
                    CustomizeText(
                        text="Ваші записи",
                    )]
            )
        ]

        for i in self.data:
            new_list.append(ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Container(
                                    width=500,
                                    padding=20,
                                    content=CustomizeText(
                                    text=f"Запис на {i['date_start']}\nПослуги:{i['services']}\nЦіна: {i['price']} грн",
                                        size=17,
                                )
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                    ft.Container(
                                        width=200,
                                        margin=ft.margin.only(bottom=20,top=10),
                                        content=CustomButton(
                                            text="Видалити",
                                            text_size=15,
                                            width=200,
                                            height=40,
                                            on_click=lambda e, id=i['id']: self.update_change(id)
                                        )
                                    )
                                    ]
                                )
                            ]
                        ))
                    )
                ]
            ))
        
        if len(self.data)==0:
            new_list=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        on_click=lambda e: self.close_modal(),
                        icon_color="#A67C52"
                    )
                ]
            ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                        width=450,
                        content=CustomizeText(text="Нажаль у вас немає записів",
                        size=20,

                            )
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            margin=ft.margin.only(top=10,bottom=20),
                            content=CustomButton(
                            width=180,
                            height=50,
                            text_size=21,
                            text="Записатися",
                            on_click=lambda e:self.go_sign()
                        ))
                    ]
                )
            ]

        return new_list


    def go_sign(self):
        if self.page.route=='/sign':
            self.close_modal()
        else:
            self.page.go('/sign')


    def update_change(self,id):
        
        self.remove_sign(id)
        self.content=ft.Column(
            width=600,
            scroll=True,
            controls=self.new_rows()
        )
        self.update()


    def close_modal(self):
        self.open=False,
        self.page.update()