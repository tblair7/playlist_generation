# Music Taste
#### Author  
#### [Tyler Blair](https://github.com/tblair7)
----
#### About
Music is an integral part of my life. To put my music finding and listening tendencies into perspective: In a matter of eight years, I reached the maximum capacity of YouTube's playlist system (5000 entries), which I didn't even know existed. Eight years of finding nearly two songs per day **on average**. Instead of examining a well laid out problem, I sought to look at something closer and more important to me, while also fostering experience in different data analysis techniques.



Initially, I thought it would be cool to analyze things like how frequently I find new music during certain times of year and think about why that might be, e.g., do I tend to find more music during the winter when I'm indoors more often due to the cold and rainy winter here in Seattle? Also, I thought to examine how different types of music persist through seasons, i.e., do the frequency components of the music I listen to correspond to each season? The number of questions I could address really bloomed once I had a better sense of what data I was working with.

My ultimate goal for this project is to be able to create playlists similar to a song I am currently enjoying. By analyzing the waveforms of songs, I am able to extract a number of audio features and find any number of its nearest neighbors to create any playlist on the fly.

 ----

##### Python Packages Utilized
- os
- numpy
- pandas
- datetime
- requests
- json
- re
- [google.oauth2.credentials](https://developers.google.com/youtube/registering_an_application)
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis "GitHub Repository")
- scikit-learn
- shutil
- pickle
- matplotlib


##### Set api_key variable
import os
os.environ['YT_API_key'] = '*your_API_key*'

----
##### Some questions I seek to examine:
- Do my music finding tendencies correlate with time of year?
  - Yes, though they're more dependent on what my work load is like.
- Does the type of music I find correlate with the time of year too?
  - Yes! The later months of the year when it starts to get cold and dark result in me finding more music!
- Do I tend to find music more quickly now than I used to, i.e., how long after a song was uploaded do I normally find the song?
  - Yes, absolutely. Sometimes I find music the same day it was uploaded, too!
- In terms of audio component analysis using the pyAudioAnalysis package, how closely correlated are the songs I listen to? Is there a large variation overall?
  - There is quite a continuum in each extracted audio feature, which isn't very surprising; I did not expect there to be hard cut-offs for genre classification.
