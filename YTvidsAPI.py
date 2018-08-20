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
import datetime

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

##### you'll need to have already set your API key as an environmental ######
##### variable before this point. If you haven't/don't want to do so   ######
##### you can simply set it explicitly here:
# api_key = {'your key'}
api_key = os.environ.get('YOUTUBE_API_KEY')

################### only parameters you should need to set ###################
# documentation of parameters you are able to use for playlistItems
# https://developers.google.com/youtube/v3/docs/playlistItems#properties

api_params_playlist = 'snippet, contentDetails' # e.g., 'id, contentDetails, statistics' as a string
playlistId = 'PLJpYtEF3No5PLMd9Z2dPtUm4CYH5xWR1y' # ID of the whatever api type you're utilizing
playlistIdentifier = 'Instrumental' # identifier for saving purposes

maxResults = 8 # 0-250, though I've set 0 to mean no maximum so I can use it for my playlist

## parameters I wish to retrieve from my playlist in the end ##
api_params_videos = "id, contentDetails, statistics, snippet"

# these will be the column headers that I select from the playlistItems df
params_playlist = 'videoId', 'videoPublishedAt', 'publishedAt', 'title'
params_playlist_rename = 'ID', 'Date Uploaded', 'Date Found', 'Title'

params_videos = 'id','channelId','viewCount','likeCount','dislikeCount', 'duration'
params_videos_rename = 'ID', 'Channel ID','Views', 'Likes', 'Dislikes', 'Duration'

##############################################################################

# sets the parameters for the API request
parameters = {"part": api_params_playlist,
              "playlistId": playlistId,
              "key": api_key}

if maxResults == 0:
    print('No maximum number of results returned')
else:
    parameters.update(dict(maxResults = maxResults))

url_playlist = "https://www.googleapis.com/youtube/v3/playlistItems"
url_videos = "https://www.googleapis.com/youtube/v3/videos"

# pulls the data from YT and puts it in a usable format
page = requests.get(url = url_playlist,
                    params = parameters) # pulls the data
j_results = json.loads(page.text) # make somewhat readable
df = pd.io.json.json_normalize(j_results['items']) # formatted table, lots of redundant info
df.columns = df.columns.map(lambda x: x.split('.')[-1])

# truncates the data based on the params_playlist input from the beginning
data_playlist = df.loc[:, df.columns.isin(list(params_playlist))]
data_playlist = data_playlist.T.drop_duplicates(keep='first').T # drop_duplicates works on rows, so transpose, select row, transpose back
data_playlist.columns = list(params_playlist_rename) # assigns column names


# saves the data_playlist structure as a .csv with a name dictated by the playlistIdentifier variable and the time
a = datetime.datetime.now().strftime('_%Y_%m_%d')
name = playlistIdentifier + time
f = open('%s.csv' % playlistIdentifier, 'w')
data_playlist.to_csv(f.name)

##############################################################################
#################  Videos API requests and data manipulation #################
##############################################################################

### start down here tomorrow

def gen_params(ID, api_params_videos, api_key):
    parameters = {"part": api_params_videos,
                  "id": ID,
                  "key": api_key}
    return parameters

def pull_YT_data(url, params):
    page = requests.get(url = url_videos,
                        params = parameters)
    j_results = json.loads(page.text)
    df = pd.io.json.json_normalize(j_results['items'])
    df.columns = df.columns.map(lambda x: x.split('.')[-1])
    return df,j_results


data_videos = pd.DataFrame([])

for vars in data_playlist.ID:
    parameters = gen_params(vars, api_params_videos, api_key)
    df = pull_YT_data(url_videos,parameters)
    data_videos = df.loc[:, df.columns.isin(list(params_videos))]
    data_videos = data_videos.T.drop_duplicates(keep='first').T
    data_videos_temp = data_videos.append(df)
    data_videos = data_videos_temp
