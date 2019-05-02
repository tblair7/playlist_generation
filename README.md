# Music Taste
#### Author  
#### [Tyler Blair](https://www.linkedin.com/in/tylerjblair)
----
#### [Personalized Playlist Generation](http://tylerblair.net/PlaylistGeneration)  
__Description:__  
With a music library of over 5,000 songs, making playlists was extremely time consuming, so I often forewent the task. Realizing that I could take a data-driven approach to this problem, I created a dynamic way of making new playlists on the fly based on a song's audio features.

First, I extracted 38 features from the raw audio waveform of each song in my musical library. Next, I needed a dynamic way to select a song from my library, especially if I couldn't quite remember the exact title/artist name. I decided to place all of my song artist/titles in a SQL database at which point I could use a loosely fitted query to help me find the song I was thinking of.  

E.g., if I knew the song I wanted was by John Mayer, I could input 'Mayer', which would find the song's ID via a loose query:  
 `"SELECT ID FROM songs WHERE title LIKE %mayer%"`

By selecting the song I desired from the results, my pipeline then uses a k-Nearest Neighbors (kNN) to find the songs with audio characteristics most similar to the selected song. In this web-hosted version of this project, a new YouTube playlist is finally created so you can listen to your new playlist! However, when run locally (separate repository), copies of these songs are moved to a new directory such that they can be listened to with your media player of choice.

__Skills/Tools:__  
_Python, AWS, Natural Language Processing (NLP), Scikit-learn (sklearn), Flask, SQL (sqlite3), Natural Language Toolkit (NLTK), [Steam API](https://steamcommunity.com/dev)_  


 ----

##### Additional requirements

- [google.oauth2.credentials](https://developers.google.com/youtube/registering_an_application)
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis "GitHub Repository")



##### Set api_key variable
import os
os.environ['YT_API_key'] = '*your_API_key*'

----
##### Some questions I also sought to examine:
- Do my music finding tendencies correlate with time of year?
  - Yes, though they're more dependent on what my work load is like.
- Does the type of music I find correlate with the time of year too?
  - Yes! The later months of the year when it starts to get cold and dark result in me finding more music!
- Do I tend to find music more quickly now than I used to, i.e., how long after a song was uploaded do I normally find the song?
  - Yes, absolutely. Sometimes I find music the same day it was uploaded, too!
- In terms of audio component analysis using the pyAudioAnalysis package, how closely correlated are the songs I listen to? Is there a large variation overall?
  - There is quite a continuum in each extracted audio feature, which isn't very surprising; I did not expect there to be hard cut-offs for genre classification.
