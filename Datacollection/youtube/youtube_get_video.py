from kaggle_clean import *
import pandas
from youtubeapi import *
import mysql.connector



yt  = Youtube()


keys = ['AIzaSyAKJ1JEhMLNB5TouvS8ugBcudrLqLLVVbU','AIzaSyAJGJji60UEE_VRk3PoFZXfNbKvsnRAc5s','AIzaSyAHSiEaazJX7RltvynvftJ2z5NFekYHO6A','AIzaSyCwjCGOpQmEHR6ttqBk4x2ERyHMqm8vgA8','AIzaSyAc6rHnrVRL0-uzro0RXNbk3GAbYcc2NMY'
        ,'AIzaSyAH6FojRnpYYTb3FbpOQSoaTLS65nDm7_I','AIzaSyB6D7-0PptA8VfZ-lWQWkfYDiKurShB4Tc','AIzaSyBldTWycDSQU7dLUR0iuLIGtRfRftCx1uM','AIzaSyBaFwF262KIlA98VHRM3sWJDNNdvDh_dcQ','AIzaSyDSvCTM3rp2K-k1H1pKeVF93EMDT67Ej0Y']

import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="whenimthinkingforthepastit_onlyyou_1121",
    database="my_database"
)


if mydb.is_connected():
        cursor = mydb.cursor()
        qry = "SELECT playlistid FROM youtube_ch_playlist"
        cursor.execute(qry)
        id_list  = [row[0] for row in cursor.fetchall()] 
        i = 0 
        j=0
        for id in id_list:
            key = keys[j]
            try:
                i+=1
                print(f'AT {i}/{len(id_list)}')

                vi_list = yt.get_video_from_playlistID(key,id)

                for v_id in vi_list:
                    insert_video_detail = """
                    INSERT INTO youtube_video (userid,videoid,video_title,likes,comments) values (%s,%s,%s,%s,%s)
                """
                    cursor.execute(insert_video_detail,yt.get_video_detail(key,v_id))
                    print('insert video in database')
            except IndexError:
                print(f"Skipping Invalid data structure") 
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
        mydb.close()



