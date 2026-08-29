import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')
API_KEY=os.getenv('API_KEY')


CHANNEL_HANDLE='WildlensbyAbrar'

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
if __name__=='__main__':
    channel_playlist_id()
    # print('channel id is executed')
else:
    print('channel id is not executed')