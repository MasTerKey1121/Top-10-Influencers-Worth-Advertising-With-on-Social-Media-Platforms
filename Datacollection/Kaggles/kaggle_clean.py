from Kaggles import kaggle
#import kaggle
import pandas as pd
from pymongo import MongoClient

class Kaggle_clean_data():
    def __init__(self):
        data_tt = kaggle.Kaggle_tt()
        data_ig = kaggle.Kaggle_ig()

        data1 = data_tt.get_final_data_tt()
        data2 = data_ig.get_final_data_ig()

        self.kaggle_result = pd.concat([data1,data2],ignore_index=True)
        self.kaggle_result.reset_index([i for i in range(0,self.kaggle_result.index[1])]).sort_values('engagement_rate',ascending=False)


        
    def get_kaggle_name(self):
        return self.kaggle_result['name']
    
    def insert_data_to_kaggle(self):
        client= MongoClient('mongodb://localhost:27017/')
        self.data_dict = self.kaggle_result.to_dict(orient="records")
        client['Kaggles']['final_data'].insert_many(self.data_dict)

    def get_kaggle_clean(self):
        print(self.kaggle_result)
        return self.kaggle_result
