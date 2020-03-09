import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
import os


def clean_text(x):
    tokens = x.split(" ")
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    return words


def get_hashtags_operations(x):
    tokens = x.split(" ")
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove break lines
    tokens = [w.replace('\n', '') for w in tokens]
    # get hashtags
    hashtags = [token for token in tokens if '#' in token]
    # clean multiple hashtags in same line
    hashtags = ['#'+hashtag.split('#')[1] for hashtag in hashtags]
    # get operation hashtags
    hashtags = [hashtag for hashtag in hashtags if '#op' == hashtag[:3]]
    return hashtags
