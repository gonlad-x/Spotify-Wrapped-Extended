import pandas as pd 
import json
import os 

def read_json_data(folder_path, encoding = 'utf-8'):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding=encoding) as file:
                json_data = json.load(file)
                data.extend(json_data)
    return data 

def create_dataframe(data):
    return pd.DataFrame(data)

df = create_dataframe(data=read_json_data('spotify_raw_data'))

grouped_bytrack_df = df.groupby('spotify_track_uri').agg(
    count = ('spotify_track_uri', 'count'),
    total_ms_played = ('ms_played', 'sum'),
    master_track_name=('master_metadata_track_name', 'first'),  
    master_artist_name=('master_metadata_album_artist_name', 'first'),  
    master_album_name=('master_metadata_album_album_name', 'first')  
).reset_index()
top_count_bytrack_df = grouped_bytrack_df.nlargest(100, 'count')
top_ms_played_bytrack_df = grouped_bytrack_df.nlargest(100, 'total_ms_played')
top_count_bytrack_df.to_csv('./tests/top_count_bytrack_output.csv', index=False)
top_ms_played_bytrack_df.to_csv('./tests/top_ms_played_bytrack_output.csv', index=False)

grouped_byartist_df = df.groupby('master_metadata_album_artist_name').agg(
    total_ms_played = ('ms_played', 'sum'),
    master_artist_name=('master_metadata_album_artist_name', 'first'), 
    count = ('spotify_track_uri', 'count'),
    total_distinct_tracks=('spotify_track_uri', 'nunique')
).reset_index()
top_count_byartist_df = grouped_byartist_df.nlargest(100, 'count')
top_ms_played_byartist_df = grouped_byartist_df.nlargest(100, 'total_ms_played')
top_count_byartist_df.to_csv('./tests/top_count_byartist_output.csv', index=False)
top_ms_played_byartist_df.to_csv('./tests/top_ms_played_byartist_output.csv', index=False)

#Check on specific artist 
#radiohead_df = df[df['master_metadata_album_artist_name'] == 'Radiohead']
#sorted_radiohead_df = radiohead_df.groupby('spotify_track_uri').agg(
#    master_track_name=('master_metadata_track_name', 'first')
#).reset_index()
#sorted_radiohead_df.to_csv('./tests/radiohead_output.csv', index=False)