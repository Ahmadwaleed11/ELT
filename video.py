import requests
import json
import os
from datetime import date 
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')
API_KEY=os.getenv('API_KEY')


CHANNEL_HANDLE='WildlensbyAbrar'
max_result=50
def channel_playlist_id():
    try:
        url=f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response=requests.get(url)
        # print (response)
        response.raise_for_status()
        data=response.json()
        # print(json.dumps(data,indent=4))
        channel_playlist=data["items"][0]
        content=channel_playlist["contentDetails"]["relatedPlaylists"]['uploads']

        print(content)
        return content
    except requests.exceptions.RequestException as e: 
        raise e 




def get_video_id(playlist_id):
    video_ids=[]
    pageToken=None
    base_url=f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_result}&playlistId={playlist_id}&key={API_KEY}'


    try:
        while True:
            url=base_url
            if pageToken:
                url+=f'&pageToken={pageToken}'

            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get('items',[]):
                video_id=item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken=data.get('nextPageToken')

            if not pageToken:
                break    
        return video_ids 
    except requests.exceptions.RequestException as e:
        raise e 


def batch_list(video_id_lst,batch_size):
    for video_id in range (0,len(video_id_lst),batch_size):
        yield video_id_lst[video_id:video_id+batch_size]

def extract_video_data(video_ids):
    extracted_data=[]
    def batch_list(video_id_lst,batch_size):
        for video_id in range (0,len(video_id_lst),batch_size):
            yield video_id_lst[video_id:video_id+batch_size]

        
    try:
        for  batch in batch_list(video_ids,max_result):
            video_ids_str=','.join(batch)
            
            url=f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get('items',[]):
                video_id=item['id']
                snippet=item['snippet']
                contentDetails=item['contentDetails']
                statistics=item['statistics']
                video_data={
                    'video_id':video_id,
                    'title':snippet['title'],
                    'publishedAt': snippet['publishedAt'],
                    'duration':contentDetails['duration'],
                    'viewCount':statistics.get('viewCount',None),
                    'likeCount':statistics.get('likeCount',None),
                    'commentCount':statistics.get('commentCount',None)
                }
                extracted_data.append(video_data)
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e 

def save_to_json(extracted_data):
    file_path=f'./data/yt_data{date.today()}.json'
    with open (file_path,'w',encoding='utf-8') as json_outfile:
        json.dump(extracted_data,json_outfile,indent=4,ensure_ascii=False)

if __name__=='__main__':
    playlist_id=channel_playlist_id()
    video_ids=get_video_id(playlist_id)
    video_data=extract_video_data(video_ids)
    save_to_json(video_data)

    
    
else:
    print('channel id is not executed')