import csv
import sys
import time
import requests
from twython import Twython, TwythonError


def getTimelineUser(user_name):

    print("Obtaining info of "+user_name)
    twitter = Twython("l1c0CeILGOfvNDKh4AFZvpIaf",
                      "dCJvCG19kUiDOe59F59zhZvxuaM8otn0gSASvBkn16X4UQhiT5")
    last_id = 0
    filecsv = csv.writer(open('timeline@'+user_name+'.csv', "w"))
    header = ['user', 'id_user', 'timestamp', 'text', 'id_tweet', 'Reply_to', 'Coordinates', 'retweets_count', 'Name', 'Location', 'Followers_Count', 'Img_URL',
              'Hashtag', 'Url', 'Favourites_Count', 'User_Mentions', 'User_Ids_Mentions', 'Favorited', 'Reply_To_UserName', 'Num_Friends', 'Listed_count', 'link_tweet']
    filecsv.writerow(header)
    try:
        timeline_results = twitter.get_user_timeline(
            screen_name=user_name, count='200')
    except TwythonError as e:
        print(e)
    for tweet in timeline_results:
        user = '@'+tweet['user']['screen_name']
        userid = tweet['user']['id']
        name = tweet['user']['name']
        location = tweet['user']['location']
        img = tweet['user']['profile_image_url']
        favorited = tweet['favorited']
        coordinates = tweet['coordinates']
        in_reply_to_user_id_str = tweet['in_reply_to_user_id_str']
        in_reply_to_screen_name = '@'+str(tweet['in_reply_to_screen_name'])
        if(in_reply_to_screen_name == '@None'):
            in_reply_to_screen_name = ''
        idstr = tweet['id_str']
        created_at = tweet['created_at']
        hashtags = ""
        mentions = ""
        mentions_id = ""
        urls = ""
        if tweet['entities']['hashtags']:
            for row in tweet['entities']['hashtags']:
                hashtags = hashtags+' #'+row['text']
        if tweet['entities']['urls']:
            for row in tweet['entities']['urls']:
                urls = urls+' '+row['url']
        if tweet['entities']['user_mentions']:
            for row in tweet['entities']['user_mentions']:
                mentions = mentions+' @'+row['screen_name']
        if tweet['entities']['user_mentions']:
            for row in tweet['entities']['user_mentions']:
                mentions_id = mentions_id+' '+row['id_str']
        text = tweet['text']
        retweet_count = tweet['retweet_count']
        favourites_count = tweet['user']['favourites_count']
        followers_count = tweet['user']['followers_count']
        listed_count = tweet['user']['listed_count']
        friends_count = tweet['user']['friends_count']
        link_tweet = f'twitter.com/{user}/status/{idstr}'
        data = [user, userid, created_at, text, idstr, in_reply_to_user_id_str, coordinates, retweet_count, name, location, followers_count,
                img, hashtags, urls, favourites_count, mentions, mentions_id, favorited, in_reply_to_screen_name, friends_count, listed_count, link_tweet]
        filecsv.writerow(data)
