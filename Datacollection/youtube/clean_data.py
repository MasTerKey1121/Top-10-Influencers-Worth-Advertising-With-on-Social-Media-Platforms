import pandas as pd
import mysql.connector


class Youtube():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",       
            user="root",             
            password="whenimthinkingforthepastit_onlyyou_1121",  
            database="my_database"
        )

    def get_clean_data(self):
        if self.mydb.is_connected():
            cursor = self.mydb.cursor()

            qry = """ select * FROM youtube_video"""

            cursor.execute(qry)

            data = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            print(df)
            cal = df.groupby('userid').agg(total_like = ('likes','sum'),total_comment = ('comments','sum') , video_count = ('videoid','count')).reset_index()
            cal = cal[cal['video_count'] > 50]
            print(cal)
            cal['like_avg'] = (cal['total_like']/cal['video_count'])
            cal['comment_avg'] = cal['total_comment']/cal['video_count']
            cal.drop(columns=['total_like','total_comment','video_count'],inplace=True)
            print(cal)




            qry = """ select * from youtube_channel"""
            cursor.execute(qry)
            yt_ch = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df_yt = pd.DataFrame(yt_ch,columns=columns)

            Youtube_er = pd.merge(df_yt,cal,on='userid')
            Youtube_er['engagement_rate'] = (Youtube_er['like_avg']+Youtube_er['comment_avg'])/Youtube_er['followers'] *100
            Youtube_er.drop(columns=['userid','like_avg','comment_avg'],inplace= True)
            #Youtube_er.rename(columns={'username':'name'},inplace=True)
            Youtube_er['source'] = 'Youtube'

            return Youtube_er.sort_values('engagement_rate')


