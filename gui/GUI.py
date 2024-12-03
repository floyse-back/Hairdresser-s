from gui.pages.add_response import add_response
from gui.pages.homepage import homepage
from gui.pages.profile_barber import profile_barber
from gui.pages.sign import sign

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.register_alert import register_alert
from gui.flet_modules.login_alert import login_alert
from gui.flet_modules.signs_alert import sign_alert


from db.db_use import db_use
from gui.settings import settings

import flet as ft

def main(page: ft.Page):
    my_homepage = homepage(page,current_width=page.width)
    my_response = add_response(page,screen_width=page.width)
    my_sign=sign(page,screen_width=page.width)
    
    container=ft.Ref[ft.Container]()
    drawer_ref=ft.Ref[ft.NavigationDrawer]()


    def handle_change(e):
        
        index=e.control.selected_index
        if page.client_storage.get("user")==None:
            if settings.route_no_register[f"{index}"]==page.route:
                return -1

            if settings.route_no_register[f"{index}"] not in ["/go_register","/go_login"]:
                page.go(f"{settings.route_no_register[f'{index}']}")
            elif settings.route_no_register[f"{index}"]=="/go_register":
                page.open(register_alert(page=page))
            elif settings.route_no_register[f"{index}"]=="/go_login":
                page.open(login_alert(page=page))
        elif page.client_storage.get("user")!=None and page.client_storage.get('panel')=='user':
            if settings.route_register[f"{index}"]==page.route:
                return -1

            if settings.route_register[f"{index}"] not in ["/go_out","/my_signs"]:
                page.go(f"{settings.route_register[f'{index}']}")
            elif settings.route_register[f"{index}"]=="/my_signs":
                user=page.client_storage.get("user")
                
                page.open(sign_alert(page=page,user=user))
            elif settings.route_register[f"{index}"]=="/go_out":
                page.client_storage.remove("user")
                page.client_storage.remove("panel")
                change_route('/go_out')
                
        elif page.client_storage.get("user")!=None and page.client_storage.get('panel')=='barber':
            if settings.route_barber[f"{index}"]==page.route:
                return -1

            if settings.route_barber[f"{index}"]!="/go_out":
                page.go(f"{settings.route_barber[f'{index}']}")
            elif settings.route_barber[f"{index}"]=="/go_out":
                page.client_storage.remove("user")
                page.client_storage.remove("panel")
                change_route("/go_leave")
                if page.route=='/profile':
                    page.go('/')
                


    def reload_drawer():
        if page.client_storage.get("user")==None:
            return ft.NavigationDrawer(
                ref=drawer_ref,
                position=ft.NavigationDrawerPosition.END,
                on_change=handle_change,
                controls=[
                    ft.NavigationDrawerDestination(label="Головна", icon=ft.icons.HOME),
                    ft.NavigationDrawerDestination(label="Залишити відгук", icon=ft.icons.REVIEWS),
                    ft.NavigationDrawerDestination(label="Записатися", icon=ft.icons.SIGNPOST),
                    ft.NavigationDrawerDestination(label="Зареєструватись", icon=ft.icons.ACCOUNT_BOX),
                    ft.NavigationDrawerDestination(label="Увійти", icon=ft.icons.LOGIN),
                ],
            )
        elif page.client_storage.get("user")!=None and page.client_storage.get('panel')=='user':
            return ft.NavigationDrawer(
                ref=drawer_ref,
                position=ft.NavigationDrawerPosition.END,
                on_change=handle_change,
                controls=[
                    ft.NavigationDrawerDestination(label="Головна", icon=ft.icons.HOME),
                    ft.NavigationDrawerDestination(label="Записи", icon=ft.icons.PERSON),
                    ft.NavigationDrawerDestination(label="Залишити відгук", icon=ft.icons.REVIEWS),
                    ft.NavigationDrawerDestination(label="Записатися", icon=ft.icons.SIGNPOST),
                    ft.NavigationDrawerDestination(label="Вийти", icon=ft.icons.ACCOUNT_BOX),
                ],
            )
        elif page.client_storage.get("user")!=None and page.client_storage.get('panel')=='barber':
            return ft.NavigationDrawer(
                ref=drawer_ref,
                position=ft.NavigationDrawerPosition.END,
                on_change=handle_change,
                controls=[
                    ft.NavigationDrawerDestination(label="Головна", icon=ft.icons.HOME),
                    ft.NavigationDrawerDestination(label="Профіль", icon=ft.icons.PERSON),
                    ft.NavigationDrawerDestination(label="Вийти", icon=ft.icons.ACCOUNT_BOX),
                ],
            )

    my_drawer=reload_drawer()

    page.theme_mode="light"
    page.theme = ft.Theme(color_scheme_seed="0xE8E8E8")
    page.padding = 0
    page.margin = 0
    page.scroll = "auto"
    page.title = "Початок"

    def resize_screen(screen):
        if page.route == "/":
            my_homepage.adaptive_width(page.width)
        elif page.route == "/add_response":
            my_response.adaptive_width(page.width)

        if page.width>730:
            if not page.client_storage.get("user"):
                container.current.content=ft.TextButton(
                content=CustomizeText(text="Зареєструватися"),
                on_click=lambda e: page.open(register_alert(page))
                )
                container.current.margin=ft.margin.only(right=80, left=120)
        elif page.width<=730:
            if not page.client_storage.get("user"):
                container.current.margin=ft.margin.only(right=0, left=0)
                container.current.content=ft.IconButton(
                icon=ft.icons.ADD,
                on_click=lambda e: page.open(register_alert(page))
                )
        
        page.update()


    def create_container():
        if page.client_storage.get("user") is not None:
            base = db_use()
            if page.client_storage.get("panel") == "user":
                user=page.client_storage.get("user")
                src = str(base.get_img(user)).replace("/static", "")
                func=lambda e: page.open(sign_alert(page=page, user=user))
            elif page.client_storage.get("panel") == "barber":
                src = str(base.get_img(user=page.client_storage.get("user"), database="barbers")).replace("../gui/static", "")
                func=lambda e: page.go('/profile')

            return ft.Container(
                width=100,
                height=100,
                content=ft.CircleAvatar(
                    foreground_image_src=f"{src}",
                    width=100,
                    height=100,
                ),
                on_click=func,
                ref=container,
                border_radius=25,
            )
        else:
            return ft.Container(
                margin=ft.margin.only(right=80, left=120),
                content=ft.TextButton(
                content=CustomizeText(text="Зареєструватися",size=15),
                on_click=lambda e: page.open(register_alert(page)),
            ),
                ref = container,
            )


    def change_route(route):
        page.views.clear()
        my_drawer = reload_drawer()
        container=create_container()

        if "/reload"==page.route:
            page.go("/")

        if "/" == page.route:
            my_homepage = homepage(page, page.width)

            page.views.append(
                ft.View(
                    route="/",
                    padding=0,
                    scroll="auto",
                    drawer=my_drawer,  # Додаємо drawer до View
                    controls=[my_homepage],
                    appbar=ft.AppBar(
                        title=ft.Container(
                            bgcolor=ft.colors.TRANSPARENT,
                            margin=ft.margin.only(left=120, top=20, bottom=10),
                            content=ft.Image(
                                src="image/logo.svg",
                                color="black",
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            on_click=lambda e: page.go("/"),
                        ),
                        actions=[
                            ft.TextButton(content=CustomizeText(text="Послуги",size=15),
                                          on_click=lambda e: my_homepage.focused_to("servises")),
                            ft.TextButton(content=CustomizeText(text="Чому ми",size=15),
                                          on_click=lambda e: my_homepage.focused_to("about")),
                            ft.TextButton(content=CustomizeText(text="Відгуки",size=15),
                                          on_click=lambda e: my_homepage.focused_to("reviews")),
                            container
                        ],
                        leading=ft.IconButton(
                            icon=ft.icons.MENU,
                            icon_size=40,
                            on_click=lambda e: page.open(my_drawer)
                        ),
                    )
                )
            )

        elif "/add_response" == page.route and page.client_storage.get("panel")!="barber":
            my_response = add_response(page, page.width)

            page.views.append(
                ft.View(
                    route="/add_response",
                    drawer=my_drawer,
                    controls=[
                        ft.AppBar(
                            title=ft.Container(
                                bgcolor=ft.colors.TRANSPARENT,
                                margin=ft.margin.only(left=120, top=20, bottom=10),
                                content=ft.Image(
                                    src="image/logo.svg",
                                    color="black",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_click=lambda e: page.go("/"),
                            ),
                            actions=[
                                ft.TextButton(content=CustomizeText(text="Головна сторінка"), on_click=lambda e: page.go("/")),
                                create_container(),
                            ],
                            leading=ft.IconButton(
                                icon=ft.icons.MENU,
                                icon_size=40,
                                on_click=lambda e: page.open(my_drawer)
                            ),
                        ),
                        my_response,
                    ],
                    scroll="auto",
                ),
            )

        elif "/sign" == page.route and page.client_storage.get('panel')!='barber':
            my_sign = sign(page, page.width)

            page.views.append(
                ft.View(
                    route="/sign",
                    drawer=my_drawer,
                    controls=[
                        ft.AppBar(
                            title=ft.Container(
                                bgcolor=ft.colors.TRANSPARENT,
                                margin=ft.margin.only(left=120, top=20, bottom=10),
                                content=ft.Image(
                                    src="image/logo.svg",
                                    color="black",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_click=lambda e: page.go("/"),
                            ),
                            actions=[
                                ft.TextButton(content=CustomizeText(text="Головна сторінка"), on_click=lambda e: page.go("/")),
                                create_container(),
                            ],
                            leading=ft.IconButton(
                                icon=ft.icons.MENU,
                                icon_size=40,
                                on_click=lambda e: page.open(my_drawer)
                            ),
                        ),
                        my_sign,
                    ],
                    scroll="auto",
                ),
            )

        elif "/profile" == page.route and page.client_storage.get('panel')=='barber':
            my_profile = profile_barber(page, page.width)

            page.views.append(
                ft.View(
                    route="/profile",
                    drawer=my_drawer,
                    controls=[
                        ft.AppBar(
                            title=ft.Container(
                                bgcolor=ft.colors.TRANSPARENT,
                                margin=ft.margin.only(left=120, top=20, bottom=10),
                                content=ft.Image(
                                    src="image/logo.svg",
                                    color="black",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_click=lambda e: page.go("/"),
                            ),
                            actions=[
                                ft.TextButton(content=CustomizeText(text="Головна сторінка"), on_click=lambda e: page.go("/")),
                                create_container(),
                            ],
                            leading=ft.IconButton(
                                icon=ft.icons.MENU,
                                icon_size=40,
                                on_click=lambda e: page.open(my_drawer)
                            ),
                        ),
                        my_profile,
                    ],
                    scroll="auto",
                ),
            )
        if (page.route=='/sign' and page.client_storage.get('panel')=='barber') or (page.route=='/add_response' and page.client_storage.get('panel')=="barber") or (page.route=='/profile' and page.client_storage.get('panel')=='user'):
            page.go('/')

        page.update()

    page.on_route_change = change_route
    page.on_resized = resize_screen
    page.go("/")

ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="static")


