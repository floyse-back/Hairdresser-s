import flet as ft

from gui.flet_modules.customize_text import CustomizeText


class footer(ft.Container):
    def __init__(self, page):
        self.page = page
        self.text_size=15
        super().__init__(
            padding=ft.padding.all(20),
            bgcolor="#A67C52",
            content=ft.Row(
                wrap=True,
                alignment="spaceEvenly",
                vertical_alignment="center",  # Вирівнювання по вертикалі
                controls=[
                    ft.Container(
                        width=400,

                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        CustomizeText(text="Контакти", color=ft.Colors.WHITE, size=self.text_size,weight="900")
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.PHONE),
                                        CustomizeText("+380968582783", color=ft.Colors.WHITE, size=self.text_size)
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        CustomizeText(text="beutisalon@gmail.com", color=ft.Colors.WHITE, size=self.text_size)
                                    ]
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        width=400,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        CustomizeText(text="Місцезнаходження", color=ft.Colors.WHITE, size=self.text_size,weight="900")
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.LOCATION_ON),
                                        CustomizeText("вулиця Келецька, 77", color=ft.Colors.WHITE, size=self.text_size)
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        CustomizeText(text="https://maps.apple.com/?address=", color=ft.Colors.WHITE, size=self.text_size)
                                    ]
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        width=400,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        CustomizeText(text="Інформація про ціни та наші пропозиції:", color=ft.Colors.WHITE, size=self.text_size,weight="900")
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            content=CustomizeText(text="https://maps.apple.com/?address=%D0%9A%D0%B5%D0%BB%D0", color=ft.Colors.WHITE, size=self.text_size),
                                            on_click=lambda event:self.page.launch_url("https://maps.apple.com/place?address=%D0%9A%D0%B5%D0%BB%D0%B5%D1%86%D1%8C%D0%BA%D0%B0%20%D0%B2%D1%83%D0%BB%D0%B8%D1%86%D1%8F,%2077,%20Vinnytsia,%20Vinnytsia%20Oblast,%2021030,%20Ukraine&ll=49.224753,28.409203&q=%D0%9A%D0%B5%D0%BB%D0%B5%D1%86%D1%8C%D0%BA%D0%B0%20%D0%B2%D1%83%D0%BB%D0%B8%D1%86%D1%8F,%2077&t=r")
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
