import flet as ft

from gui.flet_modules.customize_text import CustomizeText
from gui.flet_modules.custom_button import CustomButton
from gui.flet_modules.servise_card import servise_card
from gui.flet_modules.choice_container import choice_container
from gui.flet_modules.custom_image import custom_image
from gui.flet_modules.reviuse_card import reviuse_card
from gui.flet_modules.footer import footer


class homepage(ft.Column):
    def __init__(self,page,current_width):
        super().__init__(
            alignment=ft.alignment.center,
        )

        self.details_more=[
            "Класичні та модні стрижки",
            "Фарбування волосся",
            "Догляд за бородою та вусами",
            "Укладка та догляд"
        ]

        self.services=[
            {
                "img_src":"image/men_hair.jpg",
                "h1_text":"Чоловіча стрижка",
                "paragraph":"Завдяки увазі до деталей, ми створимо стрижку, яка відобразить вашу індивідуальність"
            },
            {
                "img_src":"image/women_hair.jpg",
                "h1_text":'Укладка',
                "paragraph":'Завдяки увазі до деталей, ми створимо стрижку, яка відобразить вашу індивідуальність.',
            },
            {
                "img_src": "image/styling.jpg",
                "h1_text": 'Фарбування',
                "paragraph": 'З нами фарби стають кращими',
            },
            {
                "img_src": "image/devices.jpg",
                "h1_text": 'Нарощування',
                "paragraph": 'Нарощуйте волося з нами',
            }
        ]

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

        self.choice_controls=self.flet_choicetext()
        self.h1_element=CustomizeText(text="Сучасна перукарня",size=58)
        self.h3_element=CustomizeText(text="Професійні послуги",size=38)
        self.paragraph_one=CustomizeText(text="Ласкаво просимо до нашої перукарні, де ваш стиль – це наша пристрасть. Наша команда професійних майстрів працює з любов'ю до деталей і бажанням створити образ, який підкреслить вашу індивідуальність.",size=16,weight="500")
        self.paragraph_two=CustomizeText(text="Ми використовуємо лише найкращі техніки й інструменти, щоб ви могли насолоджуватися результатом. Зручний онлайн-запис дозволяє легко обрати потрібний час, а затишна атмосфера салону гарантує ваш комфорт від першого кроку.",size=16,weight="500")

        self.my_footer=footer(self.page)

        self.div_header=ft.Row(
            width="100%",
            alignment="center",
            controls=[
                ft.Container(
                    margin=ft.margin.only(bottom=30,right=1),
                    content=ft.Column(
                    width=600,
                    controls=[
                        self.h1_element,
                        self.h3_element,
                        self.paragraph_one,
                        self.paragraph_two,
                        ft.Container(
                            margin=ft.margin.only(top=30,left=4),
                            content=CustomButton("Записатись"),

                        )
                    ]
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
            controls=[
            ft.Row(
            alignment="center",
            controls=[
                ft.Container(
                    alignment=ft.alignment.top_right,
                    width=480,
                    content=CustomizeText(text="Що ми пропонуємо нашим клієнтам",size=48),
                ),
                ft.Stack(
                    width=600,
                )
            ]),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Row(
                wrap=True,
                alignment="center",
                controls=self.servise_controls(),
            ),
            )
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
                            width=600,
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

        self.div_reviuse=ft.Container(
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Container(
                        width=500,
                        alignment=ft.alignment.top_right,
                        content=CustomizeText("Відгуки клієнтів", font_family="Playfair Display", size=48),
                    ),
                    ft.Row(
                        alignment=ft.alignment.center,
                        controls=[
                            reviuse_card()
                        ],
                    ),
                    ft.Container(
                        content=CustomButton(text="Залишити відгук",
                                             height=50,
                                             width=200,
                                             text_size=20,
                                             on_click=lambda event:self.page.go("/add_response")
                                             )
                    )
                ]
            )
        )

        self.view_container = ft.Container(
            width="100%",
            margin=ft.margin.only(left=25),
            content=ft.Column(
                alignment="center",
                controls=[
                    self.div_header,
                    self.div_services,
                    self.div_about,
                    self.div_choice,
                    self.div_reviuse,
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
                )
            )
        return new_list


    def adaptive_width(self,screen_width):
        print(screen_width)
        print(self.controls[0].margin)
        self.choice_ref.current.width=screen_width

        if screen_width <=450:
            print(self.controls[0].content)
            self.controls[0].content.controls[0].controls[0].content.width=400
        elif screen_width<=690:
            self.controls[0].margin=ft.margin.only(left=0)
            self.controls[0].content.controls[0].controls[0].content.width=500
        if screen_width<=800:
            self.controls[0].content.controls[0].controls[0].content.width=350
            self.controls[0].margin=ft.margin.only(left=0)
        elif screen_width<=1350:
            self.controls[0].margin=ft.margin.only(left=100)
        elif screen_width<=1240:
            #Container_Header_Text
            self.controls[0].content.controls[0].controls[0].content.width=400
            self.controls[0].margin=ft.margin.only(left=100)
        elif screen_width<=1600:
            self.controls[0].content.controls[0].controls[0].content.width=600
            self.controls[0].margin=ft.margin.only(left=100)

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