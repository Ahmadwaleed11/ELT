from airflow import DAG
import pendulum 
from datetime import datetime,timedelta

from api.video import channel_playlist_id,get_video_id,extract_video_data,save_to_json
from datawarehouse.dwh import staging_table, core_table

with DAG(
    dag_id='produce_json',
    start_date=datetime.now(),
    description='DAG to produce json file to raw data',
    schedule='0 14 * * *',
    catchup=False,
) as dag:

    # define tasks
    playlist_id = channel_playlist_id()
    video_ids = get_video_id(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(video_data)

    playlist_id >> video_ids >> video_data >> save_to_json_task



with DAG(
    dag_id='update_db',
    start_date=datetime.now(),
    description='DAG to process JSON file and insert into staging schema anad core schema',
    schedule='0 15 * * *',
    catchup=False,

) as dag:

    # define task
   update_staging = staging_table()
   update_core = core_table()

   update_staging >> update_core

