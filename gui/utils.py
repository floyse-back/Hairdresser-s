import flet as ft
from gui.flet_modules.register_alert import register_alert

def open_register(page:ft.Page):
    page.open(register_alert(page))
    page.update()
