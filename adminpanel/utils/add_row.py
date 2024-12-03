import flet as ft

from PIL import Image
import os
import uuid
import re

from gui.flet_modules.custom_button import CustomButton
from db.hashpassword import encrypt_password



class add_row(ft.Row):
    def __init__(self,page,file_picker,func_father,func_name):
        self.page=page
        self.func_father=func_father
        self.func_name=func_name

        self.file_picker = file_picker
        self.file_picker.on_result=self.file_uploaded

        self.temp=str(uuid.uuid4())

        self.username_ref = ft.Ref[ft.TextField]()
        self.name_ref = ft.Ref[ft.TextField]()
        self.position_ref = ft.Ref[ft.TextField]()
        self.phone_ref = ft.Ref[ft.TextField]()
        self.password_ref = ft.Ref[ft.TextField]()
        self.img_ref = ft.Ref[ft.Image]()
        self.register_ref=ft.Ref[ft.ElevatedButton]()

        self.tracker={
            "username":False,
            "name":False,
            "position":True,
            "phone":False,
            "password":False,
        }

        super().__init__(
            wrap=True,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=150,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                            ft.Row(controls=[ft.Image(src=f"../gui/static/barbers/noname.jpg",
                            ref=self.img_ref,
                            width=50,
                            height=50,
                            border_radius=30)],
                            alignment="center"
                            ),
                            ft.Container(
                                width=150,
                                content=CustomButton(
                                text="Завантажити зображення",
                                text_size=12,
                                width=200,
                                on_click=lambda e: self.pick_image(),
                            ),
                        ),
                        ],
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.TextField(
                            ref=self.username_ref,
                            text_size=12,
                            error_text="Мінімум 3 символа",
                            label="Введіть нікнейм",
                            on_change=lambda e:self.username_correct()
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.TextField(
                            ref=self.name_ref,
                            text_size=12,
                            label="Введіть ім'я та прізвище",
                            error_text="Приклад:Зубенко Михайло",
                            on_change=lambda e:self.name_correct()
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.TextField(
                            ref=self.position_ref,
                            text_size=12,
                            label="Введіть назву посади",
                            value="Перукар",
                            on_change=lambda e:self.position_correct()
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.TextField(
                            ref=self.phone_ref,
                            label="Введіть номер телефону",
                            input_filter=ft.InputFilter(allow=True, regex_string=r"^\+?[0-9]*$", replacement_string=""),
                            prefix_text="+380",
                            error_text="Введіть номер",
                            max_length=9,
                            on_change=lambda e:self.phone_correct()
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.TextField(
                            ref=self.password_ref,
                            error_text="Мінімум 8 символів",
                            label="Введіть пароль",
                            on_change=lambda e: self.password_correct()
                        ),
                    ),
                    ft.Container(
                        content=CustomButton(text="Додати",
                                             text_size=16,
                                             height=50,
                                             width=150,
                                             ref=self.register_ref,
                                             on_click=lambda e:self.clicked_add(),
                                             disabled=True,
                                             )
                    )
                ],
        )


    def pick_image(self):
        """Launch the FilePicker for image selection."""
        self.file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)


    def file_uploaded(self, e):
        if self.file_picker.result and self.file_picker.result.files:
            file_path = self.file_picker.result.files[0].path
            file_name = f"{self.temp}.jpg"
            save_dir = "../gui/static/barbers"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, file_name)

            with Image.open(file_path) as img:
                img = img.resize((300, 300))  # Resize to a small image
                img.save(save_path)

            

            self.img_ref.current.src=f"{save_path}"
            self.page.update()


    def file_rename(self):
        my_dir=f"../gui/static/barbers/"
        dst=str(self.username_ref.current.value)

        listdir=os.listdir(my_dir)

        for jpg in listdir:
            if jpg.endswith(".jpg") and jpg.replace(".jpg", "") == dst:
                try:
                    os.remove(f"{my_dir}{jpg}")
                except:"Виникла помилка при видалені"

        dir_src=f"{my_dir}{self.temp}.jpg"
        dir_dst=f"{my_dir}{dst}.jpg"
        os.rename(dir_src, dir_dst)


        self.img_ref.current.src=f"{dir_dst}"
        self.page.update()


    def username_correct(self):
        if len(self.username_ref.current.value)>=3:
            self.tracker["username"] = True
            self.username_ref.current.error_text=""
            data=self.func_name()
            
            if self.username_ref.current.value in data:
                self.tracker["username"] = False
                self.username_ref.current.error_text="Цей логін зайнятий"
            else:
                self.tracker["username"] = True
                self.username_ref.current.error_text=""
        else:
            self.tracker["username"] = False
            self.username_ref.current.error_text="Мінімум 3 символа"
        self.check_track()
        self.page.update()


    def password_correct(self):
        if len(self.password_ref.current.value) >= 8:
            self.tracker["password"] = True
            self.password_ref.current.error_text = ""
        else:
            self.tracker["password"] = False
            self.password_ref.current.error_text = "Мінімум 8 символів"

        self.check_track()
        self.page.update()


    def name_correct(self):
        patterns=r"^[А-ЯІЇЄҐA-Z][а-яіїєґa-z]+ [А-ЯІЇЄҐA-Z][а-яіїєґa-z]+$"

        if re.fullmatch(patterns,self.name_ref.current.value):
            self.tracker["name"]=True
            self.name_ref.current.error_text=''
        else:
            self.tracker["name"]=False
            self.name_ref.current.error_text="Приклад:Зубенко Михайло"

        self.check_track()
        self.page.update()


    def phone_correct(self):
        if len(self.phone_ref.current.value)==9:
            self.tracker['phone']=True
            self.phone_ref.current.error_text=""
        else:
            self.tracker['phone']=False
            self.phone_ref.current.error_text="Введіть остані 7 символів"

        self.check_track()
        self.page.update()


    def position_correct(self):
        if len(self.position_ref.current.value)>=3:
            self.tracker["position"]=True
            self.position_ref.current.error_text=""
        else:
            self.tracker['position']=False
            self.phone_ref.current.error_text="Мінімум 3 символи"
        self.check_track()
        self.page.update()



    def disabled_button(self,current=True):
        self.register_ref.current.disabled=current
        self.register_ref.current.update()


    def check_track(self):
        
        for i in self.tracker.values():
            if i!=True:
                self.disabled_button(current=True)
                return False
        self.disabled_button(current=False)


    def clicked_add(self):
        if self.img_ref.current.src != "../gui/static/barbers/noname.jpg":
            self.file_rename()
        password=encrypt_password(self.password_ref.current.value)
        new_data = {'username': str(self.username_ref.current.value), 'img': str(self.img_ref.current.src), 'name': str(self.name_ref.current.value), 'visiting': "0", 'position': str(self.position_ref.current.value), 'phone': str(self.phone_ref.current.value), 'password': password}
        self.func_father(new_data)
        self.reload_class()


    def reload_class(self):
        self.username_ref.current.value = ""
        self.name_ref.current.value = ""
        self.position_ref.current.value = ""
        self.phone_ref.current.value = ""
        self.password_ref.current.value = ""
        self.img_ref.current.src = "../gui/static/barbers/noname.jpg"
        self.temp=str(uuid.uuid4())
        self.username_correct()
        self.password_correct()
        self.phone_correct()
        self.position_correct()
        self.name_correct()
        self.page.update()


