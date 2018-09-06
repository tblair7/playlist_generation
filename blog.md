# Analyzing Tyler's taste in music over the years


### August 18, 2018

##### 6pm-ish

To say that music is important to me would be an understatement. Over the past 12 or so years, I've spent a lot of time finding new music on YouTube. I was never a fan of finding an artist and immediately downloading an entire album or adding it to a playlist. Instead, I hand pick each and every song- though I'll admit that there are some repeats because I rediscovered a song months or years later. During the summer of 2018, my YouTube playlist that I've continually added to since high school hit YouTube's maximum capacity for a playlist, which is 5,000 songs. I quickly did the math only to discover that, on average, I had found at least one new song per day for the past 12 years. I took to downloading these songs so that I would never lose my playlist, especially seeing as songs are sometimes removed due to DMCA claims. I used the youtube-dl package on Ubuntu to download everything from this playlist and assigned title and artist meta data so that I could easily arrange and call each file within my music player of choice.
A number of weeks later (read: last month) and after months of internal discussion, I have decided to transition out of graduate school and into a data role in industry. Because a background in chemistry doesn't give me all of the necessary skills to make this leap into data science, let alone demonstrate my ability to do just that, I figured I should tangibly expand my skill set by making a project of my own to teach myself a variety of tools while also answering some cool questions about my music taste over the years.
So, the intent of this project is to analyze my music over the years. The types of analyses will certainly depent on what forms of data I am able to extract. My current lines of thinking are:
1. What forms of meta data am I able to pull directly from YouTube given my playlist? Do all songs have assigned tags, e.g., #genre?
2. How can I go about analyzing waveforms of the files to analyze the music that way? Do I instead need .wav files as opposed to the .mp3 files that I currently have?

##### 8pm
Turns out YouTube has a nice, downloadable API to grab these data. Excitingly, these metadata include what day I added each song to my playlist. I can finally prove that I found particular songs and artists before they got big, hah!. Now I need to figure out all of the different data forms I am able to pull- total views, likes/dislikes, date uploaded, date I liked (hopefully number of views at the date that I added the song too), genres, etc.
I had never used GitHub before, so I figured this was the time to do it. I set up a SSH key so that I can work in my music_taste directory and commit changes to GitHub via the command line

##### 10pm
Now that I've established access to Google's YouTube API, I'm starting to go through what data forms I will be able to retrieve. So far, these data are as follows:
from playlistItems:

.snippet...
	.publishedAt -when added to playlist
	.title -title of video
	.channelTitle -channel uploader
	.position -where in the playlist

.contentDetails...
	.videoPublishedAt. -when the video was published by the channel uploader so I can compare with when I found the song
	.videoId - unique ID for the video so I can combine data tables if I cannot pull the playlist and video data at the same time

from videos:

.id
.contentDetails.duration
.statistics.viewCount
.statistics.likeCOunt
.statistics.dislikeCount
fileDetails.audioStreams[].bitrateBps - audio bitrate
fileDetails.audioStreams[].channelCount - number of audio channels

##### ~12am
I spent a while trying to figure out what exactly was going on in some of the examples for YT data mining, though I think that was in part because the sources were outdated. I found a part of someone's Jupyter notebook that helped me figure out how to deal with the output data because it's in a json format, which I've never worked with. Still, I think I've got it figured out enough to start working with it properly. (http://nbviewer.jupyter.org/github/twistedhardware/mltutorial/blob/master/notebooks/data-mining/2.%20YouTube%20Data.ipynb). I think this is a good place to stop for the night, seeing as I know that I won't stop once I hit that next breakthrough

### August 19, 2018

##### 11am
I eventually wish to analyze the waveforms of these songs so that I can extract trends in frequency space, but I think there will be a few hurdles along the way.
1. While I have the .mp3 files, the meta data associated with said files does not include the video ID, so I won't be able to easily match the track to its metadata entry, though it should be possible because I have -some- metadata alongside the .mp3 files.
2. I need to find a good package to work with the waveforms. I don't know exactly how these data will look, so this won't be able to be addressed fully until later..

##### 12pm
Nate just told me about Atom to more easily visualize my blog posts. Still, I wish to continue to utilize Ubuntu as much as I can so that I can become fluid in working there. Atom is  definitely easier to manage, yes, but that doesn't force me to learn.

##### 1pm
The naming structure for the different parameters I wish to retrieve from YT took me a moment to figure out. It turns out that you can't put any class properties within the call, or at least from what I've tried thus far.
e.g.,
params = ('id, contentDetails, statistics') # this is viable
params = ('id, contentDetails.duration, statistics.viewCount') # this is not viable


##### 2pm
Good progress has been made! I've made a gen_params() function that will allow me to generate the necessary structures for the API requests, regardless of what kind of request I wish to make. It also has the ability to request any number of valid data forms that particular API allows.

##### 3pm
So that I can start pushing my progress in Python to my GitHub, I need to set an environment variable of my own API key so that it's not able to be publicly viewed. It took longer than it should have because I was trying to set the environment variable via Ubuntu then access it via Python. Once I set it via Python, it was easy enough.

##### 4pm
Turns out the playlist API, despite saying that it can recognize id or playlistId, it really can only do the latter. I'm really starting to get excited about what the data will look like and what all I'll be able to do with it. The plot that's currently on my mind is how much quicker I find music nowadays, i.e., how long it takes me to add a song to a playlist vs. when it was uploaded and how that trend has changed over time. The relevant code for that will end up being built off of this line:
df.loc[:,['videoPublishedAt', 'publishedAt']
A useful resource in working with the json output format was https://stackoverflow.com/questions/34341974/nested-json-to-pandas-dataframe-with-specific-format

##### 5pm
I've taken the time to create a few functions to increase the efficiency of using this tool down the road. Now I need to figure out how I'm going to approach the problem of having all of the playlist items and their IDs but none of the meaningful video information. My current thoughts on the approach is this:
1. Much of the data that I'm pulling from the playlistItems API is really not useful to me. I should get rid of it before moving onto the video API. Still, I think some of it might be cool to use in the future, so I won't get rid of it all.
2. Because the playlistItems API gives me the ID for each video, if I iterate through these values and either create a new table to append at the end or just add the data outright, I should be pretty well off. I'm thinking I should create a new table so that it's easier to work with, especially seeing as I'll likely dump some of the data forms.
3. Items that I expect to keep at this point are, from playlistItems: id, snippet.publishedAt, snippet.channelId, snippet.title, snippet. thumbnails.maxres.url (need to check this one), contentDetails.videoId, contentDetails.videoPublishedAt

##### still 5pm
As it turns out, the thumbnails all have an extremely consistent format, which I'd be able to call later, so I'm not even going to bother with that at this point. https://i.ytimg.com/vi/EoaPhxNubL0/maxresdefault.jpg where maxresdefault lowers the quality step-wise (maxres,sd,hq,mq,default).
Also, because the conversion from json into a dataframe loses some of the higher-order attributes- thumbnails.maxres.url becomes url, alongside the other thumbnail urls- I'll have to call things more generically (and easily). Because the data I am interested in are unique in their titles and won't experience redundancy, I am not going to change the json -> dataframe conversion.
Data that I'll pull to use at this point: 'videoID', 'videoPublishedAt', 'publishedAt', 'title'
Data that I expect to pull from videos: 'videoID', 'channelId', 'views', 'likes', 'dislikes', 'channelSubscribers', waveform channels if it's possible

##### 530pm
I'm approaching 13 hours out of the past 24 that I've worked on this project and I'd like to summarize a few of my thoughts so far.
1. The number of areas that I've had to delve into has been awesome. I've learned so much already, and I'm just now getting started!
2. I need to get PyCharm back for its autofill features on packages like numpy, scipy, etc.
3. I'm curious just how many keystrokes I've made in the past 24 hours.
4. I need to parse the title into artist and song before I put it into the playlist dataframe. Selecting characters prior to the '-' ordinarily gives the artist and what's left is the song name but it isn't 100% consistent, especially in older videos. Still, I think that approach is a good place to start.

##### 8pm
videoID is apparently not as unique as I had once thought. When attempting to truncate the data table to include my four data forms, I discovered that there are four instances of videoId. I need to use a unique call to eliminate the redundant ones.

##### 9pm
I was confused for a few minutes there because YT was saying that I exceeded my number of allowed requests, when I knew very well that I shouldn't have. Apparently I had been doing a lot of my work in the notebook that wasn't actually authenticated by my api_key, which was an environment variable for my other notebook...? Perhaps I didn't actually set it as an environment variable- either that or the environment variable didn't make its way to the other notebook because that notebook was already open and running when I attempted to set the variable.


##### 11pm
I'm working on creating functions for the API requests (again) so that it doesn't need to be written multiple times in my code. For tomorrow, I need to finish that, determine how best to create a dataframe from the videoIds that I'll iterate through. Ideally, it'll just add a row for each video item. I'd like to simply iterate through the data_playlist.ID values, so that's where I'll start tomorrow.

Overall, I think this is fantastic progress for just over a day of working on the project. Soon enough I'll have a ton of data to work with that's all my own!

### August 26, 2018

##### Aftermath
Today I made a lot of progress, particularly in cleaning up the data. Where previously the dates and column names weren't very clean, I've parsed them to be more meaningful and so that I can actually work with them! Some of the dates were in nasty formats like "2010-12-14T13:29:24.000Z". I decided to convert the length of songs into seconds, though maybe I didn't need to. I also made discoveryTime in days because I don't care about that precise of a measurement for that data form.

Still, I think I'm done with the initial data structure setup unless I want to attempt to draw artist and song names from the title. The current data structure is as follows:
id, title, channelID, views, likes, dislikes, duration_secs, dateUploaded, dateFound, discoveryTime_days

I may see if I'm able to use the channelID to extract the channel name. There are a number of uploaders I'd like to track my listening tendencies over the years. I could certainly hard code channelIDs and their channel names but that's no fun and not the point of this project. I'll leave that bit until a later time though, because I want to start plotting things and also looking into the actual music files. I need to find a good Python package to help me with this.

### August 28, 2018

Two days after the fact, I realized that none of my pushes made it to GitHub. Additionally, I couldn't find the files that I had worked on and was worried that I had lost my work. However, it turns out that the branch and files were still there on my local repository but were hidden. After a bit of trouble shooting, I fixed the issue by merging my working branch, Aug26, with the master then pushing to GitHub from there. Note that the changes were already committed from the other day.

git checkout master
git merge Aug26
git push

### August 30, 2018
Had to go back over much of my script because the YT APIs only retrieve a handful of results at a time, which makes sense. Now I need to iterate through while defining a "nextToken" to grab the next page of results, all while truncating the data and appending it to the full set. Need to assign a catch for the end- NameError?

I should try to align my taste of music with big events in my life- did I prefer songs with lower frequencies when I was sad or during the winter? Did I prefer more upbeat songs during the summer?

### September 6, 2018

Because my playlist is so long and old, there are a number of corner cases that have arisen, such as the upload now being private, being flagged for spam, or being deleted all together. These corner cases are caught during different API calls and variable calls/reassignments. The df.append() function has an update soon that requires the parameters (sort = False) to work with the current version of this Notebook. The df.dropna(how = 'any') function did not drop all rows containing any NaN values, and I'm still not sure why it isn't, so I moved the drop rows call elsewhere and it works now. pyaudio was a suggested library to use for the waveform files.
