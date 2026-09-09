from airflow import DAG
import pendulum 
from datetime import datetime,timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from api.video import channel_playlist_id,get_video_id,extract_video_data,save_to_json
from datawarehouse.dwh import staging_table, core_table
from dataquality.soda import yt_elt_data_quality


staging_schema='staging'
core_schema='core'
with DAG(
    dag_id='produce_json',
    start_date=datetime.now(),
    description='DAG to produce json file to raw data',
    schedule='0 14 * * *',
    catchup=False,
) as dag_produce:

    # define tasks
    playlist_id = channel_playlist_id()
    video_ids = get_video_id(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(video_data)

    trigger_update_db= TriggerDagRunOperator(
       task_id='trigger_update_db',
       trigger_dag_id='update_db',
    )

    playlist_id >> video_ids >> video_data >> save_to_json_task >> trigger_update_db



with DAG(
    dag_id='update_db',
    start_date=datetime.now(),
    description='DAG to process JSON file and insert into staging schema anad core schema',
    schedule=None,
    catchup=False,

) as dag_update:

    # define task
   update_staging = staging_table()
   update_core = core_table()

   trigger_data_quality=TriggerDagRunOperator(
      task_id='trigger_data_quality',
      trigger_dag_id='data_quality'
   )

   update_staging >> update_core >> trigger_data_quality


with DAG(
    dag_id='data_quality',
    start_date=datetime.now(),
    description='DAG to check data quality on both layers in db ',
    schedule=None,
    catchup=False,

) as dag_quality:

    # define task
   soda_validate_staging  = yt_elt_data_quality(staging_schema)
   soda_validate_core = yt_elt_data_quality(core_schema)

   soda_validate_staging >> soda_validate_core

