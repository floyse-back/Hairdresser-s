import flet as ft

from gui.flet_modules.servise_card import servise_card

from db.db_use import db_use

class servises_cards(ft.Row,db_use):
    def __init__(self,page):
        super().__init__(
            wrap=True,
        )
        self.page=page

        self.servises=self.select_from(name="services")
        self.position_start = 0
        self.position_last = 4
        self.length_servises=len(self.servises)

        self.create_cards()

    def new_position(self,go=0):
        if go==0:
            self.position_start+=4
            self.position_last+=4
        elif go==1:
            self.position_start-=4
            self.position_last-=4


    def go_next(self):
        self.new_position(go=0)
        self.create_cards()
        self.page.update()


    def go_back(self):
        self.new_position(go=1)
        self.create_cards()
        self.page.update()


    def create_cards(self):
        self.controls.clear()

        for servise in self.servises[self.position_start:self.position_last]:
            self.controls.append(
                servise_card(
                    img_src=servise["img_src"],
                    h1_text=servise["h1_text"],
                    paragraph=servise["paragraph"],
                    price=servise["price"],
                )
            )

        self.page.update()
