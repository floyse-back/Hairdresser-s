import flet as ft
import datetime

from db.db_use import db_use

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custum_calendar import CustomCalendar

from gui.settings.settings import week_days,transform,uk_to_en


class profile_barber(ft.Column,db_use):
    def __init__(self,page,screen_width):
        super().__init__(
        )
        self.page=page
        self.screen_width=screen_width

        self.week=self.week_list()

        self.date_start=datetime.date.today()
        self.date_finish=self.date_start + datetime.timedelta(days=7)
        self.barber_table=self.select_date(barber=self.page.client_storage.get('user'),date1=self.date_start,date2=self.date_finish)
        

        self.today_container=ft.Container(
            width=450,
            content=ft.Column(
                controls=self.today_row(),
                scroll='auto',
            ),
        )
        self.table_container=ft.Container(
            content=ft.DataTable(
                column_spacing=1,
                vertical_lines=ft.BorderSide(1, color=ft.colors.GREY),
                horizontal_lines=ft.BorderSide(1, color=ft.colors.GREY),
                divider_thickness=0,
                horizontal_margin=0,
                data_row_min_height=48,
                data_row_max_height=200,
                columns=self.seven_days(),
                rows=self.table_rows()

            )
        )
        self.row=ft.ListView(
            height=2700,
            horizontal=True,
            controls=[
                self.today_container,
                self.table_container
            ]
        )

        self.my_footer=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    height=90,
                    padding=ft.padding.all(10),
                    content=ft.Text(
                        "Контакти\nМенеджер: +3809536842",
                        size=18,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ],
        )

        self.my_column=ft.Column(
            expand=True,
            controls=[
                self.row,
                self.my_footer
            ]
        )

        self.controls.append(
            self.my_column
        )

        self.thisdict=''

        self.page.update()


    def today_row(self):
        data=self.select_from(name='signs',barber=f'{self.page.client_storage.get('user')}',date=datetime.date.today())
        new_list=[
            ft.Row(
                controls=[
                    ft.Container(
                        margin=ft.margin.only(left=20,top=10,bottom=10),
                        content=CustomCalendar(width=350)
                    )
                ],
            ),
            ft.Row(
                controls=[ft.Container(
                    width=200,
                    content=CustomizeText("Сьогодні",size=22))
                          ]
            )
        ]

        for i in data:
            new_list.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            width=400,
                            content=ft.Card(
                                content=ft.Container(
                                    margin=ft.margin.all(25),
                                    content=CustomizeText(
                                        f"Ім'я: {i['name']}\nНомер: +380{i['phone']}\nДата: {i['date_start']}\nПослуги:{i['services']}\nВолосся: {i['length']}\nЦіна: {i['price']} грн",
                                        size=15,
                                    )
                                )
                            )
                        )
                    ]
                )
            )
        if len(data)==0:
            new_list.append(
                ft.Row(
                    controls=[ft.Container(
                        padding=ft.padding.only(left=10,),
                        width=400,
                        content=CustomizeText(
                            "Нажаль немає записів",
                            size=18
                        )
                    )]
                )
            )
        return new_list


    def seven_days(self):
        self.week=self.week_list()

        new_list=[
            ft.DataColumn(
                CustomizeText('  ')
            )
        ]
        for i in self.week:
            new_list.append(
                ft.DataColumn(
                    ft.Container(width=200,content=CustomizeText(f"{i}")
                )
            )
        )

        return new_list


    def table_rows(self):
        day_works=self.select_from(name='barberstimetable',timetable=f"{self.page.client_storage.get('user')}")
        new_list=[]
        work=list(day_works[0].items())[2:]

        last_list=[]
        for i in range(9,22):
            last_list.append(
                ft.DataRow(
                    cells=self.new_row(time=i,work=work)
                )
            )
        return last_list


    def new_row(self,time,work):
        new_list=[
            ft.DataCell(
                content=ft.Container(padding=5,
                                     content=CustomizeText(f"{time}:00",
                                     size=15),
                                     alignment=ft.alignment.center,
                                     )
            )
        ]
        for index,i in enumerate(self.week):
            dateday=datetime.date.today()+datetime.timedelta(days=index)
            bgcolor=self.get_color(day=i,work=work,time=time,dateday=dateday)
            if bgcolor==ft.colors.TRANSPARENT or bgcolor==ft.colors.GREEN_200:
                new_list.append(
                    ft.DataCell(
                        content=ft.Container(
                            expand=True,
                            padding=5,
                            alignment=ft.alignment.center,
                            content=CustomizeText(text=" ", weight="bold"),
                            bgcolor=bgcolor,
                        ),
                    )
                )
            else:
                new={
                    "short":'коротке',
                    "long":"довге"
                }
                new_list.append(
                    ft.DataCell(
                        ft.Container(
                            bgcolor=bgcolor,
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        content=ft.Container(
                                            width=200,
                                            alignment=ft.alignment.center,
                                            content=CustomizeText(
                                            f"Ім'я: {self.thisdict['name']}\n"
                                            f"Номер: +380{self.thisdict['phone']}\n"
                                            f"Послуги:{self.thisdict['services']}\n"
                                            f"Волосся: {new[self.thisdict['length']]}\n"
                                            f"Ціна: {self.thisdict['price']} грн"
                                        ,size=13,
                                            ))
                                    )
                                ]
                            )
                        )
                    )
                )
        return new_list


    def week_list(self):
        today = datetime.datetime.now().weekday()
        week_days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]



        week_ahead=[]
        for i in range(0,7):
            week_ahead.append(
                week_days[(i+today) % 7]
            )

        return week_ahead


    def adaptive_width(self,screen_width):
        pass


    def get_color(self,day,work,time,dateday):
        for i in work:
            time_start, time_finish = self.correct_time(day=i[0], work=i[1])
            if uk_to_en[day]==i[0] and i[1]!=None:
                test=i[1]
                if test!=None and time>=time_start and time<=time_finish:
                    if self.my_signs(dateday,time):
                        return ft.colors.GREEN_200
                    else:
                        return ft.colors.RED_200
        return ft.colors.TRANSPARENT


    def correct_time(self,day='Понеділок',work='full_day'):

        if work ==None:
            return -1,-1

        time_work=week_days[transform[day]][work]

        start_time,finish_time=time_work.replace(':00','').split('-')

        return int(start_time),int(finish_time)


    def my_signs(self,dateday,time):
        current_datetime = datetime.datetime.combine(dateday, datetime.datetime.min.time())

        new_date= current_datetime+datetime.timedelta(hours=time)

        
        for i in self.barber_table:
            date_start=i['date_start']
            date_finish=i['date_finish']
            if date_start<=new_date and new_date<date_finish:
                self.thisdict=i
                return False

        return True
