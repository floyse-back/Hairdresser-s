import flet as ft


class stars_icons(ft.Row):
    def __init__(self,size_stars,stars:int=0,**kwargs):
        self.stars_list=self.stars_list(stars)
        self.size_stars=size_stars
        super().__init__(
            controls=self.update_stars(),
            **kwargs,
        )


    def update_stars(self):
        new_list=[]
        for star in self.stars_list:
            new_list.append(
                ft.Icon(
                    name=ft.icons.STAR,
                    color=star,
                    size=self.size_stars,
                )
            )
        return new_list


    def stars_list(self,stars):
        new_list=[]
        for i in range(0,stars):
            new_list.append("#A67C52")

        while len(new_list)<5:
            new_list.append(ft.colors.GREY)
        return new_list

