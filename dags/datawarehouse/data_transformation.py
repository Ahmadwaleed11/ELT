from datetime import timedelta, datetime


def parse_duration(duration_str):
    duration_str = duration_str.replace('P', '').replace('T', '')

    components = ['D', 'H', 'M', 'S']
    values = {'D': 0, 'H': 0, 'M': 0, 'S': 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(days=values['D'], hours=values['H'], minutes=values['M'], seconds=values['S'])

    return total_duration


def transform_data(row):
    duration_td = parse_duration(row['Duration'])
    duration_time = (datetime.min + duration_td).time()
    video_type = 'Shorts' if duration_td.total_seconds() <= 60 else 'normal'

    return {
        'Video_ID': row['Video_ID'],
        'Video_Title': row['Video_Title'],
        'Upload_Date': row['Upload_Data'],
        'Duration': duration_time,
        'Video_Type': video_type,
        'Video_Views': row['Video_Views'],
        'Likes_Count': row['likes_Count'],
        'Comments_Count': row['Comments_Count'],
    }