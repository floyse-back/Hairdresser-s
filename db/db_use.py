import pymysql
import re

from db.db_configure import database_config
from db.hashpassword import encrypt_password,check_password

class db_use():
    def __init__(self):
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

    def create_row(self,name,username,email,phone,password):
        with self.connection.cursor() as cursor:
            password_crypt=encrypt_password(password)
            query="""
            INSERT INTO users (name, username, email, phone, password)
            VALUES (%s,%s,%s,%s,%s)
            """

            values=(
                name,
                username,
                email,
                phone,
                password_crypt
            )

            cursor.execute(query,values)
            self.connection.commit()
            return True

    def select_from(self,name):
        allowed_tables=["users"]

        if name not in allowed_tables:
            raise ValueError(f"Неприпустима назва таблиці: {name}")
        with self.connection.cursor() as cursor:
            query=f"""
            SELECT * FROM `{name}`
            """
            cursor.execute(query)
            return cursor.fetchall()

    def check_email(self,email):

        with self.connection.cursor() as cursor:
            query=f"""
            SELECT email FROM users
            WHERE email="{email}"
            """

            cursor.execute(query)
            output=cursor.fetchall()

            print(f"{email}")

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
                print(f"{name}")

                return True
            else:
                return False

    def loginned(self,user,password):
        email_list=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3,}$"
        if re.fullmatch(email_list,user):
            temp="email"
        else:
            temp="username"

        with self.connection.cursor() as cursor:
            query=f"""
            SELECT * FROM users
            WHERE {temp}="{user}"
            """

            cursor.execute(query)
            output=cursor.fetchall()
            print(f"{output}")
            if len(output)==1:
                if check_password(password,output[0]['password']):
                    return f"{output[0]['username']}"
                else:
                    return ""
            else:
                return ""


    def close_db(self):
        self.connection.close()
