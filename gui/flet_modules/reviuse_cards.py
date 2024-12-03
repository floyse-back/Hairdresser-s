import flet as ft
from gui.flet_modules.reviuse_card import reviuse_card

from db.db_use import db_use


class reviuse_cards(ft.Row,db_use):
    def __init__(self,page,rows):
        super().__init__(
            expand=True,
            wrap=True,
        )
        self.rows=rows
        self.page=page
        self.reviews=self.select_from("reviews")
        self.length_reviews=len(self.reviews)
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

        for review in self.reviews[self.position_start:self.position_last]:
            username=self.select_name(username=review['username'])
            self.controls.append(reviuse_card(text=review['review'],stars=review['stars'],date=review['date'],name=review['username'],username=username))


    def go_next(self):
        self.new_position(go=0)
        self.create_cards()
        self.page.update()
        self.reviews=self.select_from("reviews")



    def go_back(self):
        self.new_position(go=1)
        self.create_cards()
        self.page.update()
        self.reviews=self.select_from("reviews")
