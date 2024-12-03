import flet as ft

from db.db_use import db_use


class multi_click(ft.ExpansionTile):
    def __init__(self,page,price_ref,func,new_func=lambda:print("True")):
        self.page=page

        self.db_base=db_use()
        self.price_ref=price_ref

        self.func=func
        self.new_func=new_func
        self.new_func()

        self.price=0
        self.time=0

        self.textfield_ref=ft.Ref[ft.TextField]()
        self.radio_ref=ft.Ref[ft.RadioGroup]()
        self.servise_changed=[]
        self.h1_text=[]

        super().__init__(
            title=ft.Stack(controls=[
                                    ft.TextField(label="Послуги",
                                                 helper_text="Виберіть послугу",
                                                 ref=self.textfield_ref,
                                                 disabled=True,
                                                 multiline=True,
                                                 ),
                                ]),
            controls=[
                ft.RadioGroup(
                    ref=self.radio_ref,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[ft.Radio(
                                label="Коротке волосся",
                                value="short",
                            ),
                            ft.Radio(
                                label="Довге волосся",
                                value="long",
                            ),
                        ],
                    ),
                    value='short',
                ),
                ft.Column(
                    controls=self.create_radio()
                )
            ]
        )


    def change_list(self,value,teg):
        if value in self.servise_changed:
            self.servise_changed.remove(value)
            self.h1_text.remove(teg)
            self.change_price(value,close=False)
        else:
            self.servise_changed.append(value)
            self.h1_text.append(teg)
            self.change_price(value,close=True)



    def change_price(self,value,close=True):
        self.data=self.db_base.select_from("services")

        for i in self.data:
            if close:
                if i['value']==value:
                    self.price+=int(i['price'])
                    self.time+=int(i['time'])
            else:
                if i['value']==value:
                    self.price-=int(i['price'])
                    self.time-=int(i['time'])

        data=', '.join(self.h1_text)
        self.textfield_ref.current.value=data
        
        self.page.update()
        if callable(self.func):
            self.func()

            


    def create_radio(self):
        new_list=[]

        self.data=self.db_base.select_from("services")

        for i in self.data:
            new_list.append(
                ft.Checkbox(
                    label=f"{i['h1_text']}\t{i['price']}",
                    value=f"{i['value']}",
                    on_change=lambda e,teg=i['h1_text'], value=i["value"]:self.change_list(value,teg),
                )

            ),

        return new_list
