from db.db_use import db_use

from gui.settings.settings import week_hour,week_days
import random


class generate_timetable(db_use):
    def __init__(self,user):
        super().__init__()

        self.week_hour=week_hour
        self.week_days=week_days

        self.week_workers:dict=self.days_workers()
        self.work_time=["full_day","evening_shift","morning_shift"]
        self.time_workers=''
        self.user=user

        self.days=[]
        self.hours=[]


    def generate_days(self):
        k=3
        generate_days=[]
        self.time_workers=sorted(self.week_workers.items(),key=lambda item: item[1]["workers"])

        set_element=set()

        for i in self.time_workers[0:6]:
            set_element.add(i[1]['workers'])

        if len(set_element)==1:
            data=list(random.sample(self.time_workers,k))
            self.time_workers=data

        for i in self.time_workers:
            if len(generate_days)<3:
                generate_days.append(self.hours_workers(i))

        return self.push_db(generate_days)


    def generate_hours(self):
        new_hours=[]

        return new_hours


    def days_workers(self):
        self.barbers_time=self.select_from("barberstimetable")
        new_data={
            "monday":{
                "workers":0,
                "morning_shift":0,
                "evening_shift":0,
                "full_day":0,
            },
            "tuesday":{
                "workers":0,
                "morning_shift":0,
                "evening_shift":0,
                "full_day":0,
            },
            "wednesday":{
                "workers": 0,
                "morning_shift": 0,
                "evening_shift": 0,
                "full_day": 0,
            },
            "thursday":{
                "workers": 0,
                "morning_shift": 0,
                "evening_shift": 0,
                "full_day": 0,
            },
            "friday":{
                "workers": 0,
                "morning_shift": 0,
                "evening_shift": 0,
                "full_day": 0,
            },
            "saturday":{
                "workers": 0,
                "morning_shift": 0,
                "evening_shift": 0,
                "full_day": 0,
            },
            "sunday":{
                "workers": 0,
                "morning_shift": 0,
                "evening_shift": 0,
                "full_day": 0,
            }
        }

        false_list=['',None]

        for i in self.barbers_time:
            if i['monday'] not in false_list:
                new_data['monday']['workers']+=1
                new_data['monday'][i['monday']]+=1
            if i['tuesday'] not in false_list:
                new_data['tuesday']['workers']+=1
                new_data["tuesday"][i['tuesday']]+=1
            if i['wednesday'] not in false_list:
                new_data['wednesday']['workers']+=1
                new_data["wednesday"][i['wednesday']]+=1
            if i['thursday'] not in false_list:
                new_data['thursday']['workers']+=1
                new_data["thursday"][i['thursday']]+=1
            if i['friday']  not in false_list:
                new_data['friday']['workers']+=1
                new_data["friday"][i['friday']]+=1
            if i['saturday']  not in false_list:
                new_data['saturday']['workers']+=1
                new_data['saturday'][i['saturday']]+=1
            if i['sunday']  not in false_list:
                new_data['sunday']['workers']+=1
                new_data['sunday'][i['sunday']]+=1

        return new_data


    def hours_workers(self,data):
        day=''
        time_work=''

        if data[1]['full_day']<data[1]['evening_shift'] and data[1]['full_day']<data[1]['evening_shift']:
            time_work="full_day"
        elif data[1]['morning_shift']>data[1]['evening_shift']:
            time_work="evening_shift"
        elif data[1]['morning_shift']<data[1]['evening_shift']:
            time_work="evening_shift"
        elif data[1]['morning_shift']==data[1]['evening_shift'] and data[1]['morning_shift']==data[1]['full_day']:
            time_work=random.choice(['evening_shift','morning_shift','full_day'])
        elif data[1]['morning_shift']==data[1]['evening_shift']:
            time_work=random.choice(['evening_shift','morning_shift'])
        elif data[1]['evening_shift']==data[1]['full_day']:
            time_work=random.choice(['evening_shift','full_day'])
        elif data[1]['morning_shift']==data[1]['full_day']:
            time_work=random.choice(['morning_shift','full_day'])

        if time_work!='':
            day=data[0]

        return (day,time_work)


    def push_db(self,data):
        self.insert_table(name=f"{self.user}",day=[data[0][0],data[1][0],data[2][0]],shift=[data[0][1],data[1][1],data[2][1]])

