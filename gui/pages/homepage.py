import flet as ft


from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.servise_card import servise_card
from gui.flet_modules.choice_container import choice_container
from gui.flet_modules.custom_image import custom_image
from gui.flet_modules.footer import footer
from gui.flet_modules.div_reviuse import div_reviuse
from gui.flet_modules.div_servises import div_servises
from gui.flet_modules.custum_calendar import CustomCalendar


from db.db_use import db_use


class homepage(ft.Column,db_use):
    def __init__(self,page,current_width):
        super().__init__(
            alignment=ft.alignment.center,
        )

        self.timetable = [
            "Пн  ------------  9:00-17:00",
            "Вт  ------------  9:00-17:00",
            "Ср  ------------  9:00-17:00",
            "Чт  ------------  9:00-17:00",
            "Пт  ------------  9:00-17:00",
            "Сб  ------------  9:00-16:00",
            "Нд  ------------  9:00-13:00"
        ]

        self.details_more=[
            "Класичні та модні стрижки",
            "Фарбування волосся",
            "Догляд за бородою та вусами",
            "Укладка та догляд"
        ]

        self.services=self.select_from(name="services")

        self.choice_text=[
            "Професійні майстри: Досвідчені стилісти з багаторічним стажем.",
            "Зручний запис онлайн: Запишіться за кілька кліків.",
            "Затишна атмосфера: Розслабтеся у комфортному просторі.",
            "Високоякісні продукти: Ми використовуємо лише перевірені засоби."
        ]

        self.page=page
        self.current_width = current_width

        self.button_ref=ft.Ref[ft.ElevatedButton]()
        self.choice_ref=ft.Ref[ft.Column]()
        self.more_ref=ft.Ref[ft.Column]()
        self.details_ref=ft.Ref[ft.Column]()

        #Adaptive Ref

        #Adaptive Ref


        self.choice_controls=self.flet_choicetext()
        self.h1_element=CustomizeText(text="Сучасна перукарня",size=58)
        self.h3_element=CustomizeText(text="Професійні послуги",size=38)
        self.paragraph_one=CustomizeText(text="Ласкаво просимо до нашої перукарні, де ваш стиль – це наша пристрасть. Наша команда професійних майстрів працює з любов'ю до деталей і бажанням створити образ, який підкреслить вашу індивідуальність.",size=16,weight="500")
        self.paragraph_two=CustomizeText(text="Ми використовуємо лише найкращі техніки й інструменти, щоб ви могли насолоджуватися результатом. Зручний онлайн-запис дозволяє легко обрати потрібний час, а затишна атмосфера салону гарантує ваш комфорт від першого кроку.",size=16,weight="500")

        self.my_footer=footer(self.page)

        self.my_controls = [
            self.h1_element,
            self.h3_element,
            self.paragraph_one,
            self.paragraph_two,
        ]

        if self.page.client_storage.get('panel') != 'barber':
            self.my_controls.append(
                ft.Container(
                    margin=ft.margin.only(top=30, left=4),
                    content=CustomButton("Записатись", on_click=lambda e: self.page.go("/sign")),
                )
            )


        self.div_header=ft.Row(
            width="100%",
            alignment="center",
            controls=[
                ft.Container(
                    margin=ft.margin.only(bottom=30,right=1),
                    content=ft.Column(
                    width=600,
                    controls=self.my_controls,
                    ),
                ),
                ft.Stack(
                    width=600,
                    alignment=ft.alignment.top_right,
                    controls=[
                        custom_image(
                            src="image/woman-hairdresser-salon-1.jpg",
                        ),
                        custom_image(
                            src="image/woman-hairdresser-salon-2.jpg",
                            top=600,
                            right=150,
                        )
                    ]
                ),
            ],
        )

        self.div_services=ft.Column(
            key="servises",
            width=self.page.width,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment="center",
            controls=[
                div_servises(page=self.page)
            ]
        )
        self.div_about=ft.Container(
            margin=ft.margin.only(bottom=15,top=10),
            content=ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Row(
                    alignment="center",
                    controls=[ft.Container(
                        width=1150,
                        content=CustomizeText(text="Про нас",size=48)
                    )]
                ),
                ft.Row(
                    alignment=ft.alignment.center,
                    wrap=True,
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="image/about_img.jpg",

                            )
                        ),
                        ft.Container(
                            margin=ft.margin.only(bottom=45),
                            width=620,
                            content=ft.Column(
                                ref=self.details_ref,
                                controls=[
                                    CustomizeText(text="Перукарня для стильних і впевнених",size=32),
                                    CustomizeText(text="Ми пропонуємо повний спектр послуг для догляду за волоссям, щоб ви виглядали та почувалися бездоганно. Від класичних чоловічих та жіночих стрижок до сучасних технік фарбування – обирайте послугу, яка підходить саме вам.",size=20),
                                    ft.Column(
                                        ref=self.more_ref
                                    ),
                                    CustomButton(text="Детальніше",height=50,width=200,text_size=20,ref=self.button_ref,on_click=lambda event:self.show_more_details()),
                                    ft.Row(
                                        alignment="spaceEvenly",
                                        controls=[CustomizeText("15\nПрацівників",weight="bold",size=20,text_align="center"),
                                        CustomizeText("1606\nВідвідувачів",weight="bold",size=20,text_align="center"),
                                        CustomizeText("30\nРоків досвіду",weight="bold",size=20,text_align="center"),
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        ))

        self.choiceref_container=ft.Ref[ft.Container]()
        self.div_choice=ft.Row(
            wrap=True,
            alignment=ft.alignment.center,
            controls=[
                ft.Container(
                    ref=self.choiceref_container,
                    margin=ft.margin.only(top=1),
                    width=self.page.width,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        controls=[
                        ft.Container(
                            width=500,
                            key="about",
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                ref=self.choice_ref,
                                controls=[
                                    ft.Container(
                                        content=CustomizeText(text="Чому обрати нас",size=48,font_family="Playfair Display"),
                                        margin=ft.margin.only(bottom=40),
                                    ),
                                    ft.Container(
                                        content=CustomizeText(
                                            text="Ми піклуємося про якість послуг, комфорт клієнтів і ваш час. Обираючи нас, ви отримуєте не просто послугу, а індивідуальний підхід",
                                            font_family="Playfair Display",
                                            size=18,
                                        )
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            width=520,
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                src="image/choice_me.png",
                            )
                        )
                    ]
                )
            )
        ])

        for item in self.flet_choicetext():
            self.choice_ref.current.controls.append(item)

        if self.page.client_storage.get('panel')=='barber':
            self.check=1
        else:
            self.check=0


        self.div_reviuse=ft.Column(
            key="reviews",
            width=self.page.width,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment="center",
            controls=[div_reviuse(page=self.page,check=self.check)]
        )

        self.div_sign=(
            ft.Column(
                width=self.page.width,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment="center",
                controls=[
            ft.Row(
                alignment=ft.alignment.center,
                wrap=True,
                controls=[
                    ft.Container(
                        width=1150,
                        content=CustomizeText("Розклад",size=38),
                    ),
                ]
            ),
            ft.Row(
            wrap=True,
            alignment=ft.alignment.center,
            controls=[
                ft.Container(
                    width=500,
                    content=ft.Column(
                        controls=self.create_table()
                    )
                ),
                ft.Container(
                    content=CustomCalendar(width=250),
                )
            ]
        )
            ]
        )
        )

        self.view_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.div_header,
                    self.div_services,
                    self.div_about,
                    self.div_choice,
                    self.div_reviuse,
                    self.div_sign,
                ]
            )
        )

        self.controls.append(self.view_container)
        self.controls.append(self.my_footer)
        self.page.update()
        self.adaptive_width(self.current_width)


    def flet_choicetext(self):
        new_list=[]
        for text in self.choice_text:
            new_list.append(choice_container(text=text))
        return new_list


    def servise_controls(self):
        new_list=[]
        for servise in self.services:
            new_list.append(
                servise_card(
                    img_src=servise["img_src"],
                    h1_text=servise["h1_text"],
                    paragraph=servise["paragraph"],
                    price=servise["price"],
                )
            )
        return new_list


    def adaptive_width(self,screen_width):

        self.choice_ref.current.width=screen_width
        
        if screen_width <=450:
            self.controls[0].content.controls[0].controls[0].content.width=400
        elif screen_width<=690:
            self.controls[0].margin=ft.margin.only(left=0)
            self.controls[0].content.controls[0].controls[0].content.width=500
        if screen_width<=800:
            self.controls[0].content.controls[0].controls[0].content.width=350
            self.controls[0].margin=ft.margin.only(left=0)
        elif screen_width<=1350:
            pass
        elif screen_width<=1240:
            #Container_Header_Text
            self.controls[0].content.controls[0].controls[0].content.width=400
        elif screen_width<=1600:
            self.controls[0].content.controls[0].controls[0].content.width=620

        self.my_footer.width=screen_width

        self.page.update()


    def more_datails(self):
        new_list=[]
        for text in self.details_more:
            lst=ft.Container(
                content=CustomizeText(text=text),
                border=ft.border.only(bottom=ft.border.BorderSide(1, "black"))
            )
            new_list.append(lst)
        return new_list


    def show_more_details(self):
        self.details_ref.current.controls.pop(3)
        new_controls=self.more_datails()
        self.more_ref.current.controls=new_controls
        self.page.update()


    def create_table(self):
        new_list=[]
        for row in self.timetable:
            new_list.append(ft.Container(
                content=CustomizeText(text=f"{row}",size=24,color=ft.colors.GREY)
            ))

        return new_list

    def focused_to(self,key):
        self.scroll_to(key=key,duration=1000)

