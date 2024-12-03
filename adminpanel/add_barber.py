import flet as ft
from adminpanel.utils.barber_rows import barber_rows


def main(page: ft.Page):
    # Налаштування теми
    page.theme_mode = "light"
    page.scroll="auto"

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    barbers = barber_rows(page, file_picker)
    page.add(barbers)


ft.app(target=main, view=ft.AppView.FLET_APP)


