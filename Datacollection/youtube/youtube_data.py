from Kaggles.kaggle_clean import *

import pandas
from youtubeapi import *
import mysql.connector



yt  = Youtube()

kaggle = Kaggle_clean_data()

data = kaggle.get_kaggle_name().tolist()

keys = ['AIzaSyDhHx5obUf8Mt5XFX7uICZjG_aLmYa_sF8','AIzaSyCZRhALbHq-wsqRbeqjUX5dICsEOe-ncfw','AIzaSyDXRPbyn6TZTeX5CEMlqK8SrEAjEF4Gr20','AIzaSyBNbLgsLMk9jPjofLVpONdMHlDiWZVhWhI','AIzaSyAwzP5BQtmRfsx4FxMOVKffOYr_DG8iMs0'
       ,'AIzaSyBROYFJ_pXQkVjsPm5yMuv4oD2ztKsq7EQ','AIzaSyAMkaL17dfynS1TxWK4c1iscx95PsgggcU','AIzaSyAPB_D5lo-8Om7qsjABXGYSt4xAe2nuugo','AIzaSyDQmaWQPSbzEwbYq6fVWrTHWY5XK1FsFMI','AIzaSyADXkU8ZUYBnU9gVKaRTzF8XDxAyrsPUok']

mydb = mysql.connector.connect(
    host="localhost",       
    user="root",             
    password="whenimthinkingforthepastit_onlyyou_1121",  
    database="my_database"
)


'''
นำ ชื่อใน data ไปค้นหา uid ช่องของutube
แล้วก็นำ uid ไปหาวิดีโอเข้า database โดยเอาแค่ 100 วีดีโอต่อช่องพร้อม like comment 

ใน database youtube -> userid follower
video  -> userid video title like comment หา er rate
'''
if mydb.is_connected():
    cursor = mydb.cursor()
    print('in progress')
    i=0
    j=0
    for user in data:
        key = keys[j]
        try:
            i+= 1
            print(f'find real ch for {user} now at {i}/{len(data)}')
            ch = yt.get_channel(key,user)
            insert_youtube_channel = """
            INSERT INTO youtube_channel (userid,username,seachF,followers)
            values (%s,%s,%s,%s);
            """

            cursor.execute(insert_youtube_channel,(ch[0],ch[1],user,ch[2]))
            print(f'insert {ch[1]}')

        except IndexError:
            print(f"Skipping {user}: Invalid data structure")
            continue  
        except Exception as e:
            error_message = str(e)  # Accessing the error message as a string
            if 'quotaExceeded' in error_message:
                print("Quota out of limit.")
                j += 1
                if j >= len(keys):
                    print("Key limit reached, it's all over.")
                    break
            print(f'error {error_message}')
            continue


    mydb.commit()
    cursor.close()


