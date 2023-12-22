# Spotify Wrapped Extended

![librewolf_Af6iVmkgmh](https://github.com/gonlad-x/Spotify-Wrapped-Extended/assets/119890139/40e4972c-9be0-49da-8633-4b0b93948742)

Get your top tracks and artists since the genesis of your Spotify account. 

## Prerequisites

You need to have installed **Python** on your machine, as well as the [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) library. 

## Set up 

On your computer, create a new `spotifywrappedextended` directory. Inside this directory, create: 
* a `spotify_raw_data` subdirectory - this is where you will put your individual `Streaming_History` JSON files
* a `tests` subdirectory - this is where your Extended Wrapped files will be downloaded (as .csv)

Go to your personal Spotify account, in the [privacy settings](https://www.spotify.com/us/account/privacy/). Request your **Extended streaming history**. It should be sent to you by email 30 days or so later. 

Once you have received your **Extended streaming history** (**not** your Account data), extract the files in the `spotify_raw_data` subdirectory you created previously. 

## Usage

Download the `data.py` file you can find in this repo, at the root of your `spotifywrappedextended` directory. In your terminal, run: `py data.py`.
This will trigger the export of your top 100 artists & tracks (both by playtime and hitcount) in .csv format inside the `tests` subdirectory. 

You can then load these .csv files into any tools that support it (e.g. Google Sheets) and visualize your **Extended Spotify Wrapped**. 

