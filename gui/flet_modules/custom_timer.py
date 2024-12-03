import flet
import flet as ft


class custom_timer(ft.TimePicker):
    def __init__(self,page):
        self.page=page
        self.picker_ref=ft.Ref[ft.TimePicker]()
        super().__init__(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
            on_entry_mode_change=self.handle_entry_mode_change,
        )


    def handle_change(self,e):
        


    def handle_dismissal(self,e):
        


    def handle_entry_mode_change(self,e):
        