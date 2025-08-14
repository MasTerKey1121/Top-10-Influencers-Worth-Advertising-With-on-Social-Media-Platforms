from Kaggles.kaggle_clean import *

from youtube.clean_data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




kk = Kaggle_clean_data()
kk_data = kk.get_kaggle_clean()
yt = Youtube()
yt_data = yt.get_clean_data()

def type_byfollower(fol):
        fol = fol
        if fol > 1000000:
            return 'Mega'
        elif fol > 500000:
            return 'Macro'
        elif fol > 100000:
            return 'Mid-tier'
        elif fol > 10000:
            return 'Micro'
        elif fol > 1000:
            return 'Nano'
        
data = pd.merge(kk_data,yt_data,left_on='name',right_on='seachF',how='outer')
data['source_y'] = data['source_y'].fillna('no source')
data.drop(columns=['seachF'],inplace=True)
data.fillna(0,inplace=True)

data['engagement_rate'] = ((data['engagement_rate_x']/100 * data['followers_x']) + (data['engagement_rate_y']/100 * data['followers_y']))/(data['followers_x'] + data['followers_y'])*100
data['total_followers'] = (data['followers_x'] + data['followers_y']).astype(int)

data['type'] = data['total_followers'].apply(type_byfollower)
data.drop(columns=['engagement_rate_x','followers_x','username','followers_y','engagement_rate_y'],inplace=True)



def pieshowsource_sdis(data,ax):
    sources = pd.concat([data['source_x'], data['source_y']])
    sources = sources[sources.values != 'no source']
    percen =  sources.value_counts()
    name = percen.index.tolist()
    value = percen.values.tolist()

    ax.pie(value,labels=name, autopct = '%1.1f%%'
            ,colors = ['#833AB4','black','red'],textprops={'color': 'white','fontsize': 15,'weight':'bold'})
    ax.legend(name, title="Sources", loc="right", bbox_to_anchor=(0, 0.5))
    ax.set_title('Source Distribution')


        
def pieshowsource_d1_2(data,ax):
    group = data.groupby('source_y').size()
    group.rename(index= {'Youtube':'There are 2 Sources','no source' :'There is 1 Source'},inplace=True)
    name = group.index.tolist()
    value = (group / group.sum() *100).round(2)

    ax.pie(value,labels=name, autopct = '%1.1f%%'
            ,colors = ['red','green'],textprops={'fontsize': 15,'weight':'bold'})
    ax.legend(name, title="Sources", loc="right", bbox_to_anchor=(0, 0.7))
    ax.set_title('Distribution of Sources: 1 vs 2')

def pieshowsource_typebyfol(data,ax):
    g = data.groupby('type').size()
    name = g.index.tolist()
    value = (g / g.sum()*100).round(2)

    ax.pie(value,labels=name, autopct = '%1.1f%%'
            ,colors = 'rgb',textprops={'fontsize': 15,'weight':'bold'})
    ax.legend(name, title="Sources", loc="right", bbox_to_anchor=(0, 0.7))
    ax.set_title('Type By Followers Ratio')

def show_all_info(data):
    fig,ax = plt.subplots(1,3 ,figsize = (18,12))

    pieshowsource_sdis(data,ax[0])
    pieshowsource_d1_2(data,ax[1])
    pieshowsource_typebyfol(data,ax[2])


    plt.tight_layout()
    plt.show()


def show_by_type(data):
    # แยกประเภทข้อมูล
    data = data.sort_values('engagement_rate',ascending = False)
    mid = data[data['type'] == 'Mid-tier'].reset_index()
    macro = data[data['type'] == 'Macro'].reset_index()
    mega = data[data['type'] == 'Mega'].reset_index()

    # สร้าง subplots 3 อัน
    fig, ax = plt.subplots(3, 1, figsize=(12, 6))

    # ฟังก์ชันการ plot
    def plot_ax(ax, df, color, title):
        # ใช้ df['name'] และ df['engagement_rate'] จากข้อมูลที่มีขนาดตรงกัน (head(10))
        colors = df.apply(lambda row : color(row['source_x'],row['source_y']),axis =1)
        bars = ax.barh(df['name'].astype(str), df['engagement_rate'], color=colors)
        ax.set_title(title)
        ax.set_xlabel('Engagement rate (%)')
        ax.set_ylabel('Influencer')
        ax.bar_label(bars, fmt="%.1f", padding=5)
        handles = [
        plt.Line2D([0], [0], color='green', lw=4, label='Tiktok + Youtube'),
        plt.Line2D([0], [0], color='purple', lw=4, label='Instagram + Youtube'),
        plt.Line2D([0], [0], color='black', lw=4, label='Tiktok'),
        plt.Line2D([0], [0], color='pink', lw=4, label='Instagram')
        ]
        ax.legend(handles=handles, loc='upper left')

    # วาดกราฟสำหรับ Mid-tier, Macro, Mega
    def color(df1,df2):
        if df2 == 'Youtube':
            if df1 == 'Tiktok':
                return 'green'
            elif df1 == 'Instagram':
                return 'purple'
            return 'red'
        elif df1 == 'Tiktok':
            return 'black'
        elif df1 == 'Instagram':
            return 'pink' #สีชมพูพาสเทล
        
    plot_ax(ax[0], mid.head(10), color, f"Top 10 Mid-tier Influencers (Mean = {mid['engagement_rate'].mean():.2f})")
    plot_ax(ax[1], macro.head(10), color, f"Top 10 Macro Influencers (Mean = {macro['engagement_rate'].mean():.2f})")
    plot_ax(ax[2], mega.head(10), color, f"Top 10 Mega Influencers (Mean = {mega['engagement_rate'].mean():.2f})")

    # แสดงกราฟ
    plt.tight_layout()  
    plt.show()

show_by_type(data)
#show_all_info(data)
