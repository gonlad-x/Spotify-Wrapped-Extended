import pandas as pd 
import json
import os 
import matplotlib.pyplot as plt

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
df = df.dropna(subset=['master_metadata_track_name'])

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

df['ts'] = pd.to_datetime(df['ts']) #Convert the ts column into datetime format 
df['year_month'] = df['ts'].dt.to_period('M') #Add a new column containing the year & month, e.g. transforming '2015-12-11T18:04:19Z' into '2015-12' 
monthly_df = df.groupby('year_month').agg(
    total_ms_played=('ms_played', 'sum'),  
    total_count=('spotify_track_uri', 'count'),  
    top_track_by_ms_played=('master_metadata_track_name', lambda x: x.value_counts().idxmax()),  
    top_artist_by_ms_played=('master_metadata_album_artist_name', lambda x: x.value_counts().idxmax())  
).reset_index()
monthly_df.to_csv('./tests/monthly_output.csv', index=False)

# Plotting the graph
monthly_df['total_hours_played'] = monthly_df['total_ms_played']/3600000
x_labels = monthly_df['year_month'].astype(str)
plt.figure(figsize=(10, 6)) 
plt.plot(x_labels, monthly_df['total_hours_played'], marker='o', linestyle='-')
plt.title('Total hours played per month')  
plt.xlabel('Month')  
plt.ylabel('Total hours played')  
plt.xticks(rotation=45)  
plt.tight_layout()  
plt.show()  
