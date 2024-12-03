import flet as ft
from datetime import date, timedelta

class custom_date(ft.DatePicker):
    def __init__(self,page,ref_element,func=lambda:print("True")):
        self.page=page
        self.ref_element:ft.Ref=ref_element
        self.tomorrow = date.today() + timedelta(days=1)
        self.thirty_days_after = self.tomorrow + timedelta(days=45)
        self.func=func
        super().__init__(
            first_date=self.tomorrow,
            last_date=self.thirty_days_after,
            on_change=self.handle_change,
        )


    def handle_change(self,e):
        self.ref_element.current.value=f'{e.control.value.strftime('%Y-%m-%d')}'
        self.ref_element.current.error_text=""
        self.page.update()
        self.func()