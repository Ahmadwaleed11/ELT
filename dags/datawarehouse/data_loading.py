import json
from datetime import date
import logging

logger=logging.getLogger(__name__)

def load_data():
    file_path = f'./data/yt_data{date.today()}.json'
    try:
        logger.info(f'processing file :yt_data{date.today()}')
        with open (file_path,'r', encoding='utf-8') as raw_data:
            data=json.load(raw_data)
        return data    
    except FileNotFoundError:    
        logger.error(f'File not found:{file_path}')
        raise
    except json.JSONDecodeError:
        logger.error(f'invalid json in file:{file_path}')
        raise
