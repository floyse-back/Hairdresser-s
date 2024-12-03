from datetime import datetime

import flet as ft

from db.db_use import db_use
from gui.flet_modules.barber_row import barber_row


class barber_column(ft.Column,db_use):
    def __init__(self,page,date,price,name,phone,services,length,time_func=lambda:print("True")):
        super().__init__()

        self.page=page
        self.date = date
        self.time_func=time_func
        self.price=price

        #user_sign
        self.name=name
        self.phone=phone
        self.services=services
        self.length=length
        #user_sign


        self.day=self.date_name(self.date)
        self.time_work=''
        self.img=''
        self.create_rows()


    def create_rows(self):
        day_list=self.select_from(name="barberstimetable",day=self.day)
        new_list=[]
        for i in day_list:
            if i[f'{self.day}']!=None:
                new_list.append(i)
        

        for i in new_list:
            self.controls.append(
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        barber_row(page=self.page,user=i,price=self.price,this_date=self.date,name=self.name,phone=self.phone,services=self.services,length=self.length,time_func=self.time_func)
                    ]
                )
            )


    def time_list(self):
        new_list=[]





    def date_name(self,my_day):
        date_obj=datetime.strptime(my_day,'%Y-%m-%d').date()

        day_week=date_obj.strftime("%A").lower()
        return day_week