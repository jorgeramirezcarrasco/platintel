import csv
import json
import math
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

from utils import make_request
from utils_beautiful_soup import (
    bs_retweet_parser, bs_tweet_parser,
    bs_twitter_tweets_retweets_extractor_iterator)


def getHashtagTimeline(twitter_hashtag, tweets_dict, users_dict):
    """Function to obain the hashtag timeline from Twitter

    Arguments:
        twitter_hashtag {str} -- hashtag to extract
        tweets_dict {dict} -- dict to store tweets
        users_dict {dict} -- dict to store users

    Returns:
        dict -- dict with tweets stored
        dict -- dict with users stored
    """
    has_more_items = True
    last_tweet_id = 0
    count_tweets = 0
    proxy_active = 0
    proxy_active_value = ""
    min_position = math.inf
    try:

        # Iterate simulating scroll
        while ((has_more_items) & (count_tweets < 300)):
            print(count_tweets)
            headers = {
                'Host': 'twitter.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer': 'https://twitter.com/hashtag/'+str(twitter_hashtag)+'?f=tweets&vertical=default&src=hash',
                'X-Twitter-Active-User': 'yes',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Connection': 'keep-alive',
            }

            params = (
                ('f', 'tweets'),
                ('vertical', 'default'),
                ('q', '#'+str(twitter_hashtag)+''),
                ('src', 'hash'),
                ('lang', 'es'),
                ('max_position', str(min_position)),
                ('reset_error_state', 'false'),
            )

            url = 'https://twitter.com/i/search/timeline'
            proxy_active, proxy_active_value, page = make_request(
                proxy_active, proxy_active_value, url, headers, params)

            data = json.loads(page.content)
            min_position = data["min_position"]
            (tweets, retweets) = bs_twitter_tweets_retweets_extractor_iterator(data)
            for tweet in tweets:
                (tweets_dict, users_dict) = bs_tweet_parser(
                    tweet, tweets_dict, users_dict)
            for tweet in retweets:
                (tweets_dict, users_dict) = bs_retweet_parser(
                    tweet, tweets_dict, users_dict)

            count_tweets = count_tweets+20
            if len(tweets_dict["id_tweet"]) > 0:
                if last_tweet_id == tweets_dict["id_tweet"][-1]:
                    has_more_items = False
                last_tweet_id = tweets_dict["id_tweet"][-1]
            else:
                has_more_items = False

            time.sleep(0.1)
    except Exception as e:
        print(e)
        tweets_dict = {}
        users_dict = {}

    return tweets_dict, users_dict
