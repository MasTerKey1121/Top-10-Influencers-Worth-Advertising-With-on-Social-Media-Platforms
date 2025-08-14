from kaggle_clean import *
import pandas
from youtubeapi import *
import mysql.connector



yt  = Youtube()


key = 'AIzaSyDTSfxvuQM3qbwi713RzURDeGnJppIMBrU'

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
    
    qry = "SELECT userid FROM youtube_channel"
    cursor.execute(qry)
    
    id_list  = [row[0] for row in cursor.fetchall()] 

    in_you_ply = """
        INSERT INTO youtube_ch_playlist (userid,playlistid)
        values(%s,%s)
        """
    i=0
    for id in id_list:
        i+=1
        print(f'At {i} / {len(id_list)}')
        pyid = yt.get_playlistID(key,id)

        cursor.execute(in_you_ply,(id,pyid))
        
    mydb.commit()
    cursor.close()
    mydb.close()



