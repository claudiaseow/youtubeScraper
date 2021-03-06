import urllib3
import certifi
import json
import pandas as pd
#from googletrans import Translator
import emoji
import textblob


base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'

# change 'Grab' to what you want to search for (eg. ‘Grab+fake+app’ or ‘Grab+tutorial’), and change 'maxResults=10' to liking
remainder = 'part=snippet&maxResults=10&' + 'q=' + 'Grab' + '&key=' + api_key
url = base_url + remainder

video_id = []
title = []
description = []
published_at = []

# scraping videos related to 'Grab'
# range is the the number of pages to search through
for i in range(1):
    #opening the YouTube API
    http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url)
    response = r.data
    data = json.loads(response)
    items = data['items']
    next_page_token = data['nextPageToken']

    for item in items:
        if item['id']['kind'] == 'youtube#video':
            videoid = item['id']['videoId']
            video_id.append(videoid)
            snippet = item['snippet']
            title.append(snippet['title'])
            description.append(snippet['description'])

    url = base_url + 'pageToken=' + str(next_page_token) + '&' + remainder

# formatting data
df = pd.DataFrame(published_at, columns = ['published_at'])
df['video_id']=video_id
df['title']=title
df['description']=description
# left a giant string here for future use :)
'''
#translate data
translator = Translator()
translated = []
for row in df['title']:
    try:
        translated.append(translator.translate(row).text)
    except ValueError:
        translated.append('translate manually')

df['title_translated']=translated

#getting comments
comments = []
#get top rated comments for each video
for id in df['video_id']:
    dict = {}
    #adjust maxResults to liking
    video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?maxResults=50&part=snippet%2C+replies&order=relevance&videoId=' + str(id) + '&key=' + api_key
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', video_link)
    response = r.data
    data = json.loads(response)
    items = data['items']

    for item in items:
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
        channel_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
        dict[channel_id]=[comment]
    for i, j in dict.items():
        #remove emojis
        row = ''.join(j)
        new_row = ''.join(c for c in row if c not in emoji.UNICODE_EMOJI)
        try:
            #translate
            translated = translator.translate(new_row).text
            dict[i].append(translated)
        except ValueError:
            dict[i].append('translate manually')
    comments.append(dict)

df['comments']=comments
'''

df.to_csv('/Users/mingjun.lim/Documents/youtubeScraper/test.csv')