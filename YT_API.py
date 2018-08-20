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

maxResults = 2 # 0-250, though I've set 0 to mean no maximum so I can use it for my playlist

## parameters I wish to retrieve from my playlist in the end ##
#params_videos = "id, contentDetails, statistics"
#params_playlist = "snippet,contentDetails" # playlist ID needed?

##############################################################################


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

page = requests.get(url = url,
                    params = parameters)

#page_playlist = requests.request(method = "get",
#                                 url = url_videos,
#                                 params=parameters_playlist) # if I change how I handle multiple requests

j_results = json.loads(page.text)

########## if you wish to visualize what data was actually retrieved ##########
print (page.text)


df = pd.io.json.json_normalize(j_results['items'])
df.columns = df.columns.map(lambda x: x.split('.')[-1])
