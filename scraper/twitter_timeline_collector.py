import csv
import sys
import time
import requests
from twython import Twython, TwythonError
from utils import read_from_env_file


def getTimelineUser(user_name, tweets_dict):
    """Function to obain the user timeline from Twitter API

    Arguments:
        user_name {str} -- user name to extract
        tweets_dict {dict} -- dict to store tweets

    Returns:
        dict -- dict with tweets stored
    """

    print("Obtaining info of "+user_name)
    env_vars = read_from_env_file()
    twitter = Twython(env_vars['TWYTHON_KEY'],
                      env_vars['TWYTHON_PASS'])
    last_id = 0

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
        replies_count = 0
        if tweet['entities']['user_mentions']:
            replies_count = len(tweet['entities']['user_mentions'])
            for row in tweet['entities']['user_mentions']:
                mentions_id = mentions_id+' '+row['id_str']
        text = tweet['text']
        retweet_count = tweet['retweet_count']
        favourites_count = tweet['user']['favourites_count']
        followers_count = tweet['user']['followers_count']
        listed_count = tweet['user']['listed_count']
        friends_count = tweet['user']['friends_count']
        link_tweet = f'twitter.com/{user}/status/{idstr}'
        # Output tweets
        tweets_dict["id_tweet"].append(
            idstr if idstr else "")
        tweets_dict["id_user"].append(
            userid if userid else "")
        tweets_dict["user"].append(
            user if user else "")
        tweets_dict["link_tweet"].append(
            link_tweet if link_tweet else "")
        tweets_dict["timestamp"].append(
            created_at if created_at else "")
        tweets_dict["text"].append(
            text if text else "")
        tweets_dict["replies_count"].append(
            replies_count if replies_count else "")
        tweets_dict["retweets_count"].append(
            retweet_count if retweet_count else "")
        tweets_dict["likes_count"].append(
            favourites_count if favourites_count else "")

    return tweets_dict
