import flet as ft

from adminpanel.utils.create_row import create_row
from db.db_use import db_use
from gui.flet_modules.custom_button import CustomButton
from db.generate_work import generate_timetable


from adminpanel.utils.add_row import add_row



class barber_rows(ft.Column, db_use):
    def __init__(self, page,file_picker:ft.FilePicker):
        self.page = page
        self.file_picker = file_picker
        self.file_picker.on_result=self.file_uploaded


        if not hasattr(self.page, "overlay"):
            self.page.overlay = []

        self.page.overlay.append(self.file_picker)
        super().__init__(alignment=ft.MainAxisAlignment.CENTER)

        self.add_element=add_row(self.page,self.file_picker,func_father=self.new_barber,func_name=self.collect_username)


        self.register_ref=ft.Ref[ft.ElevatedButton]()

        self.controls.append(
            self.add_element
        )

        self.create_rows(init=1)

    def create_rows(self, init=0):
        self.info = self.select_from("barbers")
        for i in self.info:
            row = create_row(i, self.page, self.file_picker)
            self.controls.append(row)
        if init == 0:
            self.page.update()


    def new_barber(self,new_data):
        timetable=generate_timetable(new_data['username'])
        timetable.generate_days()
        self.insert_barber(username=new_data['username'],password=new_data['password'],name=new_data['name'],phone=new_data['phone'],img=new_data['img'],position=new_data['position'])
        row = create_row(new_data, self.page, self.file_picker)
        self.controls.append(row)
        self.page.update()


    def collect_data(self):
        all_data = []
        for row in self.controls:
            if isinstance(row, create_row):
                all_data.append(row.collect_data())
        return all_data


    def collect_username(self):
        all_name = []
        for row in self.controls:
            if isinstance(row, create_row):
                all_name.append(row.collect_data()['username'])
        return all_name


    def file_uploaded(self, e):
        pass


