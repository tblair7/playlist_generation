################### YouTube API Data Extraction with Python ###################
############################# Author: Tyler Blair #############################

# This script will pull data from YouTube using their APIs. To do this,
# you will have to set up API credentials with Google, which can be easily
# done at console.developers.google.com

# Additionally, this script pulls the YouTube API key from your system's
# environmental variables. If you are unfamiliar with how to do this, I
# have included the steps in the README.md file on my GitHub (tblair7)

import os

import requests
import json
from datetime import datetime
import pandas as pd

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

##### you'll need to have already set your API key as an environmental ######
##### variable before this point. If you haven't/don't want to do so   ######
##### you can simply set it explicitly here: api_key = {'your key'}    ######
api_key = os.environ.get('YOUTUBE_API_KEY')

################### only parameters you should need to set ###################
# documentation of parameters you are able to use for playlistItems
# https://developers.google.com/youtube/v3/docs/playlistItems#properties

api_type = 'playlistItems' # e.g., videos, playlistItems, search as a string
api_params = 'snippet, contentDetails' # e.g., 'id, contentDetails, statistics' as a string
id = 'PLJpYtEF3No5PLMd9Z2dPtUm4CYH5xWR1y' # ID of the whatever api type you're utilizing

maxResults = 8 # 0-250, though I've set 0 to mean no maximum so I can use it for my playlist

## parameters I wish to retrieve from my playlist in the end ##
#params_videos = "id, contentDetails, statistics"

# these will be the column headers that I select from the playlistItems df
params_playlist = 'videoId', 'videoPublishedAt', 'publishedAt', 'title'
params_playlist_rename = 'ID', 'Date Uploaded', 'Date Found', 'Title'

##############################################################################

# This may be changed later once I decide if I really want to just make the playlist workup linear
if api_type == 'playlistItems':
    parameters = {"part": api_params,
                  "playlistId": id,
                  "key": api_key}
else:
    parameters = {"part": api_params,
                  "playlistId": id,
                  "key": api_key}

if maxResults == 0:
    print('No maximum number of results returned')
else:
    parameters.update(dict(maxResults = maxResults))


url_base = "https://www.googleapis.com/youtube/v3/"
url = url_base + api_type

# pulls the data from YT and puts it in a usable format
page = requests.get(url = url,
                    params = parameters) # pull
j_results = json.loads(page.text) # make somewhat readable
df = pd.io.json.json_normalize(j_results['items']) # formatted table, lots of redundant info
df.columns = df.columns.map(lambda x: x.split('.')[-1])

# truncates the data based on the params_playlist input from the beginning
data_playlist = df.loc[:, df.columns.isin(list(params_playlist))]
data_playlist = data_playlist.T.drop_duplicates(keep='first').T # drop_duplicates works on rows, so transpose, select row, transpose back
data_playlist.columns = list(params_playlist_rename) # assigns column names
