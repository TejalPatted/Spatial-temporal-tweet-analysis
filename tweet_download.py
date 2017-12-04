# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 00:46:22 2017

@author: Tejal
"""

import tweepy
import sys
import jsonpickle
import os
from datetime import datetime
consumer_key = "YNGMUTo3MXehTkg6S4uhEUlVN"
consumer_secret = "8z0ZyVdeXk8bQna9SgT6rz0YxOoxeFM7IUNy9lmZFWruUfPgex"
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)
searchQuery = 'happy OR enjoy OR fun OR glad OR joy'  # this is what we're searching for
maxTweets = 20000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets_1021_2.txt'
sinceId = None
max_id = -1L
tweetCount = 0
lat = 34.0522
lon = -118.2437
max_r =10
until = "2017-10-21"
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,until=until
                                            ,geocode = "%f,%f,%dmi" % (lat, lon, max_r))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            if(tweetCount%1000==0):
                    print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


import json
i = 0
with open(fName, 'r') as f:
    l = []
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            l.append(tweet['coordinates'])
            i = i+1

l1 = []
for i in l:
    l1.append(i['coordinates'])
    
import numpy as np
np.savetxt("coord.csv", l1, delimiter=",")
