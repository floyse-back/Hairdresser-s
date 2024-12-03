import os
import random

def avatar_random(gender):

    if gender=="men":
        img=r"\static\avatars\men"
    elif gender=="women":
        img=r"\static\avatars\women"

    dir=os.listdir(os.getcwd()+img)

    return img+'\\'+random.choice(dir)



