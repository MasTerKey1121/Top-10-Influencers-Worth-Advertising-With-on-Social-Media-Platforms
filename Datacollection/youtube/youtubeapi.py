from googleapiclient.discovery import build

class Youtube():
    def __init__(self):
        pass


    def get_channel(self,key,qe):
        youtube = build("youtube", "v3", developerKey=key)

        request = youtube.search().list(part="snippet", type="channel", q=qe, maxResults=5)
        response = request.execute()

        channel = []
        result = []
        for ch in response['items']:
            id = ch['snippet']['channelId']
            re_sta = youtube.channels().list(part="statistics", id=id)
            res_sub = re_sta.execute()
            sub = int(res_sub['items'][0]['statistics']['subscriberCount'])
            name = ch['snippet']['title']
            channel.append([id,name,sub])
        if channel:
            result = max(channel, key=lambda x: x[2])

        return result
    
    def get_playlistID(self,key,id):
        youtube = build("youtube", "v3", developerKey=key)

        request = youtube.channels().list(part="contentDetails",id=id)
        response = request.execute()

        pyid = response['items'][0]['contentDetails']["relatedPlaylists"]['uploads']

        return pyid

    def get_video_from_playlistID(self,key,pid):
        next_page_token = None
        youtube = build("youtube", "v3", developerKey=key)
        videoidlist =[]
        while len(videoidlist) < 200:
            request = youtube.playlistItems().list(part="snippet",playlistId=pid,maxResults=50,pageToken = next_page_token)
            response = request.execute()

            for item in response['items']:
                videoidlist.append(item['snippet']['resourceId']['videoId'])


            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        return videoidlist
    
    def get_video_detail(self,key,videoid):
        youtube = build("youtube", "v3", developerKey=key)
            
        request = youtube.videos().list(part="snippet,statistics",id=videoid)
        data = request.execute()
        chid = data['items'][0]['snippet']['channelId']
        vid = data['items'][0]['id']
        title = data['items'][0]['snippet']['title']
        like = data['items'][0]['statistics']['likeCount']
        comment = data['items'][0]['statistics']['commentCount']

        return (chid,vid,title,like,comment)

"""
หาvideo ลง db โดยใช้การวนลูปของ video ในลิสทีละ 1 video


"""
