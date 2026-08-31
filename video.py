import requests
import json
import os
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
    





if __name__=='__main__':
    # playlist_id=channel_playlist_id()
    # print(get_video_id(playlist_id))
    
    print('channel id is executed')
else:
    print('channel id is not executed')