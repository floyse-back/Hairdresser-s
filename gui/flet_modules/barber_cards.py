import flet as ft

from gui.flet_modules.barber_card import barber_card

from db.db_use import db_use


class barbers_cards(ft.Row,db_use):
    def __init__(self,page,rows):
        super().__init__(
            expand=True,
            wrap=True,
        )
        self.rows=rows
        self.page=page
        self.barbers=self.select_from("barbers")
        self.length_barbers=len(self.barbers)
        self.position_start=0
        self.position_last=rows
        self.create_cards()

    def new_position(self,go=0):
        if go==0:
            self.position_start+=self.rows
            self.position_last+=self.rows
        elif go==1:
            self.position_start-=self.rows
            self.position_last-=self.rows


    def create_cards(self):
        self.controls.clear()

        for barber in self.barbers[self.position_start:self.position_last]:
            
            
            self.controls.append(barber_card(img=barber["img"],name=barber['name'],username=barber['username'],position=barber['position']))


    def go_next(self):
        self.new_position(go=0)
        self.create_cards()
        self.page.update()
        self.barbers=self.select_from("barbers")


    def go_back(self):
        self.new_position(go=1)
        self.create_cards()
        self.page.update()
        self.barbers=self.select_from("barbers")