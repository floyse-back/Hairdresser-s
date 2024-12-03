import flet as ft

from db.db_use import db_use
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.customize_text import CustomizeText
from gui.settings.settings import week_days,transform

from datetime import datetime, timedelta

class barber_row(ft.Card,db_use):
    def __init__(self,page,user,this_date,price,name,phone,services,length,time_func=lambda:print("True")):
        super().__init__(
            width=700,
        )
        self.user=user
        self.page=page

        #user_sign
        self.name=name
        self.phone=phone
        self.services=services
        self.length=length
        #user_sign

        self.page.snack_bar=ft.SnackBar(
            duration=2000,
            content=ft.Row(
                alignment="center",
                controls=[CustomizeText("Ви успішно записались",
                                  size=20,
                                  weight="700",
                                  color=ft.colors.WHITE,
                                  )
            ]
            )
        )

        self.radio_ref=ft.Ref[ft.RadioGroup]()
        self.button_ref=ft.Ref[ft.ElevatedButton]()

        self.time=time_func()

        
        self.this_date=this_date
        self.thisday=list(self.user.keys())[1]
        self.time_work=self.user[f'{self.thisday}']
        self.price=price
        self.username=self.user['username']
        self.user_info=self.select_userinfo(
            username=self.username,
        )[0]
        self.img=self.user_info['img'].replace('../gui/static','')

        self.content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(top=4, left=5),
                                    content=ft.CircleAvatar(
                                        background_image_src=f"{self.img}",
                                        width=100,
                                        height=100
                                    )
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            margin=ft.margin.only(top=4),
                                            content=CustomizeText(text=f"{self.user_info['name']}", size=17),
                                        ),
                                        ft.Container(
                                            content=CustomizeText(text=f"{self.user_info['position']}", size=13,
                                                                  color=ft.colors.GREY)
                                        )
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(left=25),
                                    content=CustomizeText(
                                        text=f"Виберіть час запису",
                                        size=16,
                                    ),
                                )
                            ]
                        ),
                        ft.Row(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(ft.RadioGroup(
                                    ref=self.radio_ref,
                                    on_change=lambda e:self.open_button(),
                                    content=ft.Row(
                                        wrap=True,
                                        width=500,
                                        controls=self.create_radio()
                                    )
                                ),)
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(left=25),
                                    content=CustomizeText(
                                    text=f"Приблизний час: {self.correct_time()}",
                                    color=ft.colors.GREY,
                                    size=18
                                ))
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(left=25),
                                    content=CustomizeText(
                                    text=f"Приблизна ціна: {self.price} грн",
                                    color=ft.colors.GREY,
                                    size=18
                                )
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[ft.Container(
                                margin=ft.margin.only(top=5, bottom=15),
                                content=CustomButton(text="Записатися",
                                                     on_click=lambda e:self.click_button(),
                                                     ref=self.button_ref,disabled=True, text_size=16, width=200, height=50),
                        )]
                        )
                    ]
                )


    def create_radio(self):
        new_list=[]
        hours=self.create_timetable()
        for i in hours:
            new_list.append(
                ft.Radio(
                    width=150,
                    value=f"{i}",
                    label=f"{i}:00",
                )
            )
        if len(new_list)>0:
            return new_list
        elif len(new_list)==0:
            return new_list.append(
                CustomizeText(
                    text="Нажаль все зайнято"
                )
            )


    def create_timetable(self):
        my_time=week_days[f"{transform[f'{self.thisday}']}"][f"{self.time_work}"]
        time_start,time_finish=my_time.split('-')

        signs=self.select_from(name="signs",barber=f"{self.username}",date=self.this_date)
        start_hour=int(time_start.split(':')[0])
        end_hour=int(time_finish.split(':')[0])

        hours = [hour for hour in range(start_hour, end_hour+1)]

        for row in signs:
            hour_start,hour_finish=row['date_start'].hour,row["date_finish"].hour
            minute_start,minute_finish=row['date_start'].minute,row["date_finish"].minute
            if hour_finish==hour_start:
                hours.remove(hour_start)
            elif hour_finish-hour_start>0:
                t=0
                if minute_finish!=0:
                    t=1
                for i in range(hour_start,hour_finish+t):
                    hours.remove(i)

        last_list=[]
        time_hour = self.time // 60
        tracker=True

        for i in range(0,len(hours)):
            if len(hours)-1>i+time_hour:
                if self.time%60!=0:
                    test=i+time_hour-1
                else:
                    test=i+time_hour
                for s in range(i,test):
                    if hours[s+1]-hours[s]==1:
                        tracker=True
                    else:
                        tracker=False
                        break
                if tracker:
                    last_list.append(hours[i])

                tracker=True

        return last_list


    def correct_time(self):
        hour_time=int(self.time//60)
        minute_time=self.time%60
        hour=""
        minute=''

        if hour_time==1:
            hour="година"
        elif hour_time>=2 and hour_time<=4:
            hour="години"
        else:
            hour="годин"

        if minute_time==1:
            minute="хвилина"
        elif minute_time>2 and minute_time<=4:
            minute="хвилини"
        else:
            minute="хвилин"

        if self.time<60:
            return f"{self.time} {minute}"
        elif self.time>=60:
            return f"{self.time//60} {hour} {self.time%60} {minute}"


    def open_button(self):
        if self.radio_ref.current.value!='':
            self.button_ref.current.disabled=False
        else:
            self.button_ref.current.disabled=True

        self.page.update()


    def click_button(self):
        time_start=f"{self.radio_ref.current.value}:00"
        time=self.time
        time_finish=self.add_time(time_start,time)

        date_start = datetime.strptime(f"{self.this_date} {time_start}", "%Y-%m-%d %H:%M")
        date_finish=datetime.strptime(f"{self.this_date} {time_finish}","%Y-%m-%d %H:%M")
        barber=self.username
        name=self.name
        phone=self.phone
        price=self.price
        length=self.length
        services=self.services
        if self.page.client_storage.get('user'):
            user=self.page.client_storage.get('user')
        else:
            user=None
        


        self.insert_sign(name=name,phone=phone,date_start=date_start,date_finish=date_finish,barber=barber,services=services,price=price,length=length,user=user)
        self.page.snack_bar.open=True
        self.page.go('/')


    def add_time(self,time_str,add):
        time_obj=datetime.strptime(time_str,'%H:%M')

        new_time=time_obj+timedelta(minutes=int(add))
        return new_time.strftime('%H:%M')


