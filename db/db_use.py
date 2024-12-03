import pymysql
import re
from datetime import datetime


from db.db_configure import database_config
from db.hashpassword import encrypt_password,check_password
from db.img_randomer import avatar_random

class db_use():
    def __init__(self):
        super().__init__()
        self.host=database_config['host']
        self.user=database_config['user']
        self.password=database_config['password']
        self.database=database_config['database']
        self.connection=self.connect_db()


    def connect_db(self):
        return pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               )


    def remove_item(self,item):
        query=""


    def update_db(self):
        pass


    def get_img(self,user:str,database="users"):
        with self.connection.cursor() as cursor:
            query=f"""SELECT img FROM {database}
            WHERE username="{user}"
            """
            cursor.execute(query)
            return cursor.fetchall()[0]['img']


    def create_row(self,name,username,email,phone,password,gender):
        with self.connection.cursor() as cursor:
            password_crypt=encrypt_password(password)
            img=avatar_random(gender=gender).replace("\\","/")
            query="""
            INSERT INTO users (name, img, username, email, phone, password,gender)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            values=(
                name,
                img,
                username,
                email,
                phone,
                password_crypt,
                gender
            )

            cursor.execute(query,values)
            self.connection.commit()
            return True


    def select_userinfo(self,username):
        with self.connection.cursor() as cursor:
            query="""
            SELECT * FROM barbers 
            WHERE username=%s
            """
            values=(username,)

            cursor.execute(query,values)
            return cursor.fetchall()


    def select_from(self,name,username=None,barber=None,date=None,day=None,timetable=None):
        allowed_tables=["users","services","reviews","barbers","barberstimetable","signs"]

        if name not in allowed_tables:
            raise ValueError(f"Неприпустима назва таблиці: {name}")

        with self.connection.cursor() as cursor:
            if day != None and name=="barberstimetable":
                query=f"""
                SELECT username,`{day}` FROM `{name}`
                """
            elif name=="users" and username!=None:
                query=f"""
                SELECT * FROM `{name}`
                WHERE username='{username}'
                """
            elif name=="signs" and date!=None and barber!=None:
                query=f"""
                SELECT * FROM signs
                WHERE barber="{barber}"
                  AND date_start BETWEEN '{date} 00:00:00' AND '{date} 23:59:59';
                """
            elif name=="signs" and date==None and barber!=None:
                query=f"""
                SELECT * FROM signs
                WHERE barber="{barber}"
                """
            elif name=="barberstimetable" and timetable!=None:
                query=f"""
                SELECT * FROM {name}
                WHERE username='{timetable}'
                """
            elif name=="reviews":
                query=f"""
                SELECT * FROM `{name}`
                ORDER BY date DESC;
                """
            else:
                query=f"""
                SELECT * FROM `{name}`
                """


            cursor.execute(query)
            return cursor.fetchall()


    def remove_sign(self,id):
        with self.connection.cursor() as cursor:
            query="""
            DELETE FROM sign
            WHERE id=%s;
            """

            values=(id,)
            cursor.execute(query,values)
            self.connection.commit()


    def update_sign(self):
        pass


    def check_email(self,email):

        with self.connection.cursor() as cursor:
            query=f"""
            SELECT email FROM users
            WHERE email="{email}"
            """

            cursor.execute(query)
            output=cursor.fetchall()


            if len(output)!=0:
                return True
            else:
                return False


    def check_name(self,name):

        with self.connection.cursor() as cursor:
            query=f"""
            SELECT email FROM users
            WHERE username="{name}"
            """

            cursor.execute(query)
            output=cursor.fetchall()

            if len(output)!=0:

                return True
            else:
                return False


    def loginned(self,user,password,type):
        email_list=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3,}$"
        if type=="barber":
            name_base="barbers"
            temp="username"
        else:
            name_base="users"
            if re.fullmatch(email_list,user):
                temp="email"
            else:
                temp="username"

        with self.connection.cursor() as cursor:
            query=f"""
            SELECT * FROM {name_base}
            WHERE {temp}="{user}"
            """

            cursor.execute(query)
            output=cursor.fetchall()

            if len(output)==1:
                if check_password(password,output[0]['password']):
                    return f"{output[0]['username']}"
                else:
                    return ""
            else:
                return ""


    def reviews_insert(self,username,review,stars):
        this_date=datetime.now()


        formated_date=this_date.strftime('%Y-%m-%d %H:%M:%S')
        with self.connection.cursor() as cursor:
            query="""
                INSERT INTO reviews (username,review,date,stars)
                VALUES (%s,%s,%s,%s)
                """
            values=(username,review,formated_date,int(stars))

            cursor.execute(query,values)
            self.connection.commit()


    def delete_barber(self,name):
        with self.connection.cursor() as cursor:
            query=f"""
            DELETE FROM barbers
            WHERE username="{name}"
            """
            cursor.execute(query)
            self.connection.commit()
        self.delete_timetable(name)


    def delete_timetable(self,name):
        with self.connection.cursor() as cursor:
            query=f"""
            DELETE FROM barberstimetable
            WHERE username="{name}"
            """
            cursor.execute(query)
            self.connection.commit()



    def insert_table(self,name,day,shift):
        """
        for i in len(0,3):
            if shift[i] not in ['evening_shift','morning_shift','full_day']:
                raise ValueError(f"Неприпустимий графік: {shift}")
            if day[i] not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                raise ValueError(f"Неприпустима день тижня: {day}")
        """
        
        with self.connection.cursor() as cursor:
            query=f"""
            INSERT INTO barberstimetable (username,{day[0]},{day[1]},{day[2]}) 
            VALUES ("{name}","{shift[0]}","{shift[1]}","{shift[2]}")
            """

            cursor.execute(query)
            self.connection.commit()

    def insert_barber(self,username,password,name,phone,img="../gui/static/barbers/noname.jpg",visiting=0,position="Перукар"):
        with self.connection.cursor() as cursor:
            query="""
            INSERT INTO barbers (username,img,name,visiting,phone,position,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            values=(username,img,name,visiting,phone,position,password)
            cursor.execute(query,values)
            self.connection.commit()


    def select_name(self,username):
        with self.connection.cursor() as cursor:
            query="""
            SELECT name FROM users
            WHERE username=%s
            """
            values=(username,)
            cursor.execute(query,values)
            return cursor.fetchall()[0]['name']


    def select_date(self,barber,date1,date2):
        date1=datetime.combine(date1,datetime.min.time())
        date2=datetime.combine(date2,datetime.max.time())
        
        

        with self.connection.cursor() as cursor:
            query="""
            SELECT * FROM signs
            WHERE barber=%s and
            date_start BETWEEN %s AND %s;
            """
            values=(barber,date1,date2)
            cursor.execute(query,values)

            return cursor.fetchall()


    def select_usersign(self,username):
        with self.connection.cursor() as cursor:
            query="""
            SELECT * FROM signs
            WHERE user=%s
            """
            values=(username,)
            cursor.execute(query,values)
            return cursor.fetchall()


    def remove_sign(self,id):
        with self.connection.cursor() as cursor:
            query="""
            DELETE FROM signs
            WHERE id=%s
            """

            values=(id,)
            cursor.execute(query,values)

            self.connection.commit()


    def insert_sign(self,name,phone,date_start,date_finish,barber,services,length,price,user=None):
        with self.connection.cursor() as cursor:
            query="""
            INSERT INTO signs (name,phone,date_start,date_finish,barber,services,length,price,user)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            value=(name,phone,date_start,date_finish,barber,services,length,price,user)

            cursor.execute(query,value)
            self.connection.commit()


