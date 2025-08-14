from pymongo import MongoClient
import pandas as pd
import re
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

class Kaggle_tt:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')



    def change_string_M_K(self,data):
        patternM = '[Mm]$'
        patternK = '[Kk]$'
        bool_M = bool(re.search(patternM, data))
        bool_K = bool(re.search(patternK, data))
        if bool_M:
            data = float(data.replace('M',''))
            data = data*1000000
        elif bool_K:
            data = float(data.replace('K',''))
            data = data*1000
        else:
            return data
        return data

    def get_clean_dec(self):
        filter_dec={'Rank': {'$ne': None}}

        result_dec = self.client['Kaggles']['Tiktok_data'].find(filter_dec)

        df_dec = pd.DataFrame(list(result_dec))

        df_dec['like_avg'] = df_dec['likes(avg'].apply(lambda x : x.get(')',{}))
        df_dec['comment_avg'] = df_dec['comments(avg'].apply(lambda x : x.get(')',{}))
        df_dec['share_avg'] = df_dec['shares(avg'].apply(lambda x : x.get(')',{}))

        df_dec.drop(columns=['Tiktok name','likes(avg','comments(avg','shares(avg','views(avg)'],inplace=True)
        df_dec.rename(columns={'Tiktoker name':'name','Rank':'number'},inplace=True)

        df_dec['followers'] = df_dec['followers'].apply(self.change_string_M_K).astype(int)
        df_dec['like_avg'] = df_dec['like_avg'].apply(self.change_string_M_K).astype(int)
        df_dec['comment_avg'] = df_dec['comment_avg'].astype(str).apply(self.change_string_M_K).astype(int)
        df_dec['share_avg'] = df_dec['share_avg'].astype(str).apply(self.change_string_M_K).astype(int)

        return df_dec

    def get_clean_nov(self):
        filter_nov={'row-cell': {'$ne': None}}

        result_nov = self.client['Kaggles']['Tiktok_data'].find(filter_nov)

        df_nov = pd.DataFrame(list(result_nov))

        df_nov.drop(columns=['Views (Avg'],inplace=True)
        df_nov['\r\nFollowers']= df_nov['\r\nFollowers'].apply(self.change_string_M_K).astype(int)
        df_nov['Likes'] = df_nov['Likes'].apply(self.change_string_M_K).astype(int)
        df_nov['Comments'] = df_nov['Comments'].apply(self.change_string_M_K).astype(int)
        df_nov['Shares'] = df_nov['Shares'].apply(self.change_string_M_K).astype(int)

        df_nov.rename(columns={'row-cell':'number','Tiktoker name':'name'
                            ,'\r\nFollowers':'followers','Likes':'like_avg','Comments':'comment_avg','Shares':'share_avg'},inplace=True)
        

        return df_nov

    def get_clean_sep(self):
        filter_sep={'S.no': {'$ne': None}}

        result_sep = self.client['Kaggles']['Tiktok_data'].find(filter_sep)

        df_sep = pd.DataFrame(list(result_sep))

        df_sep['S'] = df_sep['S'].apply(lambda x : x.get('no',{})).astype(int)
        df_sep['Likes avg'] = df_sep['Likes avg'].apply(lambda x:x.get('',{}))
        df_sep['Comments avg'] = df_sep['Comments avg'].apply(lambda x:x.get('',{}))
        df_sep['Shares avg'] = df_sep['Shares avg'].apply(lambda x:x.get('',{}))


        df_sep['Subscribers'] = df_sep['Subscribers'].apply(self.change_string_M_K).astype(int)
        df_sep['Likes avg'] = df_sep['Likes avg'].apply(self.change_string_M_K).astype(int)
        df_sep['Comments avg']= df_sep['Comments avg'].astype(str).apply(self.change_string_M_K).astype(int)
        df_sep['Shares avg'] = df_sep['Shares avg'].astype(str).apply(self.change_string_M_K).astype(int)

        df_sep.drop(columns=['Tiktok name','Views avg'],inplace=True)
        df_sep.rename(columns = {'S':'number','Tiktoker name':'name','Subscribers':'followers'
                                ,'Comments avg':'comment_avg','Likes avg':'like_avg','Shares avg':'share_avg'},inplace=True)

        return df_sep


    def get_all_clean_data(self):
        df_sep = self.get_clean_sep()
        df_nov = self.get_clean_nov()
        df_dec = self.get_clean_dec()

        df = pd.concat([df_sep,df_nov,df_dec],ignore_index=True)

        df['number'] = df.index +1
        df.dropna(inplace=True)
        return df

    def get_final_data_tt(self):
        data = self.get_all_clean_data()

        data['engagement_rate'] = ((data['like_avg'] + data['comment_avg'])/data['followers']) *100

        #
        counted = data.groupby('name').size().reset_index(name='counts')


        er = data.groupby('name')['engagement_rate'].sum().reset_index()
    
        #
        followers = data.groupby('name')['followers'].first().reset_index()
      
        #
        self.result = pd.merge(er, counted, on='name')
        self.result = pd.merge(self.result, followers, on='name')

        #
        self.result['engagement_rate'] = self.result['engagement_rate'] / self.result['counts']
        self.result.drop(columns=['counts'],inplace=True)
        self.result['source']  = 'Tiktok'
    

        #เอาข้อมูลที่ไม่น่าเชื่อถือออกหรือ er >30%
        self.result = self.result[self.result['engagement_rate']<30]
        return self.result.sort_values('engagement_rate',ascending=False)



'''
มีข้อมูลที่ดูเวอร์เกินไปต้องตัดทิ้งด้วย

'''

class Kaggle_ig:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.filter_dec={
            'Rank': {
                '$ne': None
            }
        }

        self.filter_sep={
            'S.no': {
                '$ne': None
            }
        }
        self.filter_nov={
            's.no': {
                '$ne': None
            }
        }


        self.result_dec = self.client['Kaggles']['Instagram_data'].find(
        filter=self.filter_dec
        )

        self.result_sep = self.client['Kaggles']['Instagram_data'].find(
        filter=self.filter_sep
        )
        self.result_nov = self.client['Kaggles']['Instagram_data'].find(
        filter=self.filter_nov
        )



        self.df_dec = pd.DataFrame(list(self.result_dec))
        self.df_sep = pd.DataFrame(list(self.result_sep))
        self.df_nov = pd.DataFrame(list(self.result_nov))


    def change_string_M_K(self,data):
        patternM = '[Mm]$'
        patternK = '[Kk]$'
        bool_M = bool(re.search(patternM, data))
        bool_K = bool(re.search(patternK, data))
        if bool_M:
            data = float(data.replace('M',''))
            data = data*1000000
        elif bool_K:
            data = float(data.replace('K',''))
            data = data*1000
        return data



    def clean_data_dec(self):
        self.df_dec["engagement_avg"] = self.df_dec["Eng"].apply(lambda x: x.get(" (Avg", {}).get(")", None))
        self.df_dec.drop(columns=['instagram name','Category_1','Category_2','country','Eng'],inplace=True)
        #add fucntion ที่แปลง M และ K กับเปลี่ยน type ของข้อมูล
        self.df_dec.dropna(inplace=True)
        self.df_dec.rename(columns={'Rank':'number'},inplace=True)
        self.df_dec['followers'] = self.df_dec['followers'].apply(self.change_string_M_K).astype(int)
        self.df_dec['engagement_avg'] = self.df_dec['engagement_avg'].apply(self.change_string_M_K).astype(int)
        self.df_dec.reindex(columns=['number','name','followers','engagement_avg'])

    def clean_data_sep(self):
        self.df_sep['S'] = self.df_sep['S'].apply(lambda x: x.get("no", None))
        self.df_sep.drop(columns=[' Name','Category_1','Authentic engagement\n','Audience country'], inplace=True)
        self.df_sep.dropna(inplace=True)
        self.df_sep.rename(columns={'S':'number','Instagram name':'name','Subscribers':'followers','Engagement average\r\n':'engagement_avg'}, inplace=True)
        self.df_sep.reindex(columns=['number','name','followers','engagement_avg'])    
        self.df_sep['followers'] = self.df_sep['followers'].apply(self.change_string_M_K).astype(int)
        self.df_sep['engagement_avg'] = self.df_sep['engagement_avg'].apply(self.change_string_M_K).astype(int)

    def clean_data_nov(self):
        self.df_nov['s'] = self.df_nov['s'].apply(lambda x: x.get("no", None))
        self.df_nov.rename(columns={'s':'number','Name':'name','Followers':'followers'},inplace=True)
        self.df_nov['engagement_avg'] = self.df_nov['Eng'].apply(lambda x: x.get(" (Avg", {}).get(")", None))
        self.df_nov.drop(columns=['Instagram Name','Category-1','\nCountry','Eng'],inplace= True)
        self.df_nov.dropna(inplace=True)
        self.df_nov.reindex(columns=['name','followers','engagement_avg'])
        self.df_nov['followers'] = self.df_nov['followers'].apply(self.change_string_M_K).astype(int)
        self.df_nov['engagement_avg'] = self.df_nov['engagement_avg'].apply(self.change_string_M_K).astype(int)
 


    def clean_data_all(self):
        self.clean_data_dec()
        self.clean_data_sep()
        self.clean_data_nov()

        df = pd.concat([self.df_dec, self.df_sep, self.df_nov], ignore_index=True)
        df['number'] = df.index + 1
        print(df)
        return df

    def get_final_data_ig(self):
        data = self.clean_data_all()
        data['engagement_rate'] = (data['engagement_avg']/data['followers'])*100
        count = data.groupby('name').size().reset_index(name='counts')
        er = data.groupby('name')['engagement_rate'].sum().reset_index(name = 'engagement_rate')
        follower = data.groupby('name')['followers'].first().astype(int)
        self.result = pd.merge(er,count,on='name')
        self.result = pd.merge(self.result,follower,on='name')
        self.result['engagement_rate'] = self.result['engagement_rate']/self.result['counts']
        self.result.drop(columns=['counts'],inplace= True)
        self.result['source'] = 'Instagram'
        self.result.sort_values(by='engagement_rate',ascending=False,inplace= True)
        self.result = self.result[self.result['engagement_rate']<30]

        return self.result


