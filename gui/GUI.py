import flet as ft

from gui.pages.add_response import add_response
from gui.pages.homepage import homepage
from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.register_alert import register_alert


def main(page:ft.Page):
    my_homepage = homepage(page,page.width)
    my_response = add_response(page,page.width)

    page.theme_mode="light"
    page.theme = ft.Theme(color_scheme_seed="0xE8E8E8")
    page.padding=0
    page.margin=0
    page.scroll="auto"
    page.title="Початок"
    page.update()

#+380973557006

    def resize_screen(screen):
        print(page.width)
        if page.route=="/":
            my_homepage.adaptive_width(page.width)
        elif page.route=="/add_response":
            my_response.adaptive_width(page.width)

    def change_route(route):
        page.views.clear()
        if "/"==page.route:
            page.views.append(
                ft.View(
                    route="/",
                    padding=0,
                    scroll="auto",
                    controls=[
                        ft.AppBar(
                            title=ft.Container(
                                bgcolor=ft.Colors.TRANSPARENT,
                                margin=ft.margin.only(left=120,top=20,bottom=10),
                                content=ft.Image(
                                src="image/logo.svg",
                                color="black",
                                fit=ft.ImageFit.CONTAIN,
                            )
                            ),
                            actions=[
                                ft.TextButton(content=CustomizeText(text="Послуги")),
                                ft.TextButton(content=CustomizeText(text="Чому обрати нас")),
                                ft.TextButton(content=CustomizeText(text="Зв'язок")),
                                ft.Container(margin=ft.margin.only(right=80,left=120),content=ft.TextButton(
                                    content=CustomizeText(text="Зареєструватися"),
                                    on_click=lambda e: page.open(register_alert(page)),
                                )),
                            ]
                          ),
                        my_homepage,
                    ]
                ),
            )
        elif "/add_response"==page.route:
            print("Hello World")
            page.views.append(
                ft.View(
                    route="/",
                    scroll="auto",
                    controls=[
                        ft.AppBar(
                            title=ft.Container(
                                bgcolor=ft.Colors.TRANSPARENT,
                                margin=ft.margin.only(left=120, top=20, bottom=10),
                                content=ft.Image(
                                    src="image/logo.svg",
                                    color="black",
                                    fit=ft.ImageFit.CONTAIN,
                                )
                            ),
                            actions=[
                                ft.TextButton(content=CustomizeText(text="Послуги")),
                                ft.TextButton(content=CustomizeText(text="Чому обрати нас")),
                                ft.TextButton(content=CustomizeText(text="Зв'язок")),
                                ft.Container(margin=ft.margin.only(right=80, left=120),
                                             content=ft.TextButton(content=CustomizeText(text="Зареєструватися"))),
                            ]
                        ),
                        my_response,
                    ]
                ),
            )
        elif "/sign"==page.route:
            pass
        elif "/user_account"==page.route:
            pass


        page.update()

    page.on_route_change=change_route
    page.on_resized=resize_screen
    page.go("/")

ft.app(target=main,view=ft.WEB_BROWSER,assets_dir="static")
