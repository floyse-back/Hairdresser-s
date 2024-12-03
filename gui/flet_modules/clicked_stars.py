import flet as ft

from gui.flet_modules.customize_text import CustomizeText


class clicked_stars(ft.Container):
    def __init__(self):
        self.stars=0
        self.markers=["Погано","Так собі","Нормально","Добре","Відмінно"]
        self.colors_stars=["grey","grey","grey","grey","grey"]
        super().__init__(
            content=ft.Row(
                wrap=True,
                controls=self.create_forelements()
            )
        )

    def create_forelements(self):
        new_list=[]
        for index,i in enumerate(self.markers):
            new_list.append(ft.Container(
                    width=70,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.STAR,
                                icon_size=30,
                                icon_color=ft.colors.GREY,
                                on_click=lambda event,my_index=index:self.render_stars(my_index+1)
                            ),
                            CustomizeText(i,
                                  color=ft.colors.GREY,size=12,text_align="center",
                          ),
                   ]
                ))
            )
        return new_list

    def switch_colors(self):
        for index,element in enumerate(self.content.controls):
            element.content.controls[0].icon_color=self.colors_stars[index]
            element.content.controls[1].icon_color=self.colors_stars[index]
        self.update()

    def render_stars(self,star_selected):
        self.colors_stars=["grey","grey","grey","grey","grey"]
        for i in range(0,star_selected):
            self.colors_stars[i]="#A67C52"
        self.stars=star_selected
        self.switch_colors()

