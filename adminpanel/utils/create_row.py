import flet as ft
from PIL import Image
import os

from gui.flet_modules.customize_text import CustomizeText
from db.db_use import db_use


class create_row(ft.Column,db_use):
    def __init__(self, data, page, file_picker):
        self.page = page
        self.data = data
        self.file_picker = file_picker

        self.information=''

        self.username_ref = ft.Ref[ft.TextField]()
        self.name_ref = ft.Ref[ft.TextField]()
        self.visiting_ref = ft.Ref[ft.TextField]()
        self.position_ref = ft.Ref[ft.TextField]()
        self.phone_ref = ft.Ref[ft.TextField]()
        self.password_ref = ft.Ref[ft.TextField]()
        self.img_ref = ft.Ref[ft.Image]()

        super().__init__(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=CustomizeText(f"Дані про: {data['position']} {data['name']}")
                        )
                    ]
                ),
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    controls=[
                        ft.Container(
                            height=150,
                            width=150,
                            content=ft.Image(
                                src=f"{data["img"]}",
                                ref=self.img_ref,
                                height=150,
                                width=150,
                                border_radius=30,

                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.username_ref,
                                value=f"{data['username']}",
                                text_size=12,
                                disabled=True,
                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.name_ref,
                                value=f"{data['name']}",
                                disabled=True,
                                text_size=12,
                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.visiting_ref,
                                value=f"{data['visiting']}",
                                disabled=True,
                                text_size=12,
                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.position_ref,
                                value=f"{data['position']}",
                                disabled=True,
                                text_size=12,
                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.phone_ref,
                                value=f"{data['phone']}",
                                disabled=True,
                            ),
                        ),
                        ft.Container(
                            width=150,
                            content=ft.TextField(
                                ref=self.password_ref,
                                value=f"{data['password']}",
                                disabled=True,
                            ),
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                on_click=lambda e: self.delete_row(),
                            )
                        ),
                    ],
                ),
            ]
        )
        self.remove_jpg()

    def pick_image(self):
        self.file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)


    def file_uploaded(self, e):
        if self.file_picker.result and self.file_picker.result.files:
            file_path = self.file_picker.result.files[0].path
            file_name = f"{self.data['username']}.jpg"
            save_dir = "../gui/static/barbers"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, file_name)

            with Image.open(file_path) as img:
                img = img.resize((50, 50))
                img.save(save_path)

            self.data["img"] = save_path
            

            # Update widget (you can use a label or notification here)
            ft.Text("Image uploaded and updated!", color=ft.colors.GREEN)
            self.page.update()


    def delete_row(self):
        if self in self.parent.controls:
            self.parent.controls.remove(self)
            self.delete_barber(name=str(self.username_ref.current.value))
            self.parent.update()


    def remove_jpg(self):
        information=self.select_from("barbers")
        barbers_img=os.listdir("../gui/static/barbers")

        correct_barbers=[]
        name=["noname"]

        for row in information:
            name.append(row['username'])

        for i in barbers_img:
            correct_barbers.append(i.replace(".jpg", ""))

        for i in correct_barbers:
            if i not in name:
                try:
                    os.remove("../gui/static/barbers/"+i+'.jpg')
                except Exception as ex:
                    



    def collect_data(self):
        row_data = {
            'username': self.username_ref.current.value,
            'name': self.name_ref.current.value,
            'visiting': self.visiting_ref.current.value,
            'position': self.position_ref.current.value,
            'phone': self.phone_ref.current.value,
            'password': self.password_ref.current.value,
            'img': self.img_ref.current.src,
        }
        return row_data

