# -*- encoding: utf-8 -*-
import csv
import datetime
import functools
import json
import os
import re
import string
import sys
import time
from datetime import datetime

import nltk
import numpy as np
import pandas as pd
import requests
from nltk.corpus import stopwords

from twitter_hashtag_collector import get_hashtag_timeline
from twitter_timeline_collector import get_timeline_user
from utils import (clean_text, create_dict_from_structure, filter_anon_hashtag,
                   filter_anon_username, get_hashtags_operations)


def collect(term):
    """Function to execute a search on twitter from the initial term

    Arguments:
        term {str} -- Value to search
    """
    tweets_dict = create_dict_from_structure('tweets_hashtag')
    users_dict = create_dict_from_structure('users_hashtag')

    tweets_dict, users_dict = get_hashtag_timeline(
        term, tweets_dict, users_dict)

    users_df = pd.DataFrame(users_dict)

    users_anon_df = users_df
    users_anon_df['anon'] = users_df['username'].apply(
        lambda x: filter_anon_username(x))
    users_anon_df = users_anon_df.loc[users_anon_df['anon'] == 1, ]
    users_anon_df = users_anon_df.drop_duplicates(subset='username')
    users_visited = []
    for index, row in users_anon_df.iterrows():
        tweets_dict = get_timeline_user(str(row['username'][1:]), tweets_dict)
        users_visited.append(row['username'])
        time.sleep(2)

    tweets_df = pd.DataFrame(tweets_dict)

    # Remove duplicates

    tweets_df = tweets_df.drop_duplicates(subset='id_tweet')

    # Extract operations to perform another extraction iteration over the associated campaigns found

    tweets_df['clean_text'] = tweets_df['text'].map(lambda x: clean_text(x))
    tweets_df['hashtags'] = tweets_df['text'].map(
        lambda x: get_hashtags_operations(x))
    tweets_df['operations'] = tweets_df['hashtags'].map(lambda x: True if len(
        [hashtag for hashtag in x if '#op' == hashtag[:3]]) > 0 else False)
    top_hashtags_df = tweets_df[tweets_df['operations'] ==
                                True]['hashtags'].explode().value_counts().to_frame()
    hashtags_df = top_hashtags_df[top_hashtags_df['hashtags'] > 3].reset_index(
    )
    hashtags_df['anon'] = hashtags_df['index'].apply(
        lambda x: filter_anon_hashtag(x, term))
    hashtags = hashtags_df.loc[hashtags_df['anon'] == 1, ]['index']

    for hashtag in hashtags:
        print(hashtag)
        hashtag = hashtag[1:]
        tweets_dict, users_dict = get_hashtag_timeline(
            hashtag, tweets_dict, users_dict)
        users_df = pd.DataFrame(users_dict)
        users_anon_df = users_df
        if 'username' in list(users_df.columns):
            users_anon_df['anon'] = users_df['username'].apply(
                lambda x: filter_anon_username(x))
            users_anon_df = users_anon_df.drop_duplicates(subset='username')
            users_anon_df = users_anon_df.loc[users_anon_df['anon'] == 1, ]
            for index, row in users_anon_df.iterrows():
                if row['username'] not in users_visited:
                    tweets_dict = get_timeline_user(
                        str(row['username'][1:]), tweets_dict)
                    time.sleep(2)

    # Store final results
    tweets_df = pd.DataFrame(tweets_dict)
    date_str = str(datetime.now()).split(' ')[0]
    tweets_df.to_csv(f'./results_{term}_{date_str}.csv', index=False)


def main():
    if(len(sys.argv) != 1):
        collect(term=sys.argv[1])
    else:
        print("Incorrect use, please write a Timeline. Example 'python3 twitter_collector.py duomo'")


if __name__ == "__main__":
    main()
