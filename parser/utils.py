import json
import string

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords


def clean_text(x):
    """Function to clean the text for processing

    Arguments:
        x {str} -- input text

    Returns:
        list -- list of cleaned words
    """
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


def transform_date(x):
    """Function to transform a date

    Arguments:
        x {str} -- input timestamp

    Returns:
        pd.Timestamp -- timestamp processed
    """
    try:
        date = pd.Timestamp(x)
    except:
        date = pd.Timestamp(int(x))
    return date


def get_hashtags_operations(x):
    """Function to extract the hashtag from the text

    Arguments:
        x {str} -- input text

    Returns:
        list -- extracted hashtags
    """
    tokens = x.split(" ")
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove break lines
    tokens = [w.replace('\n', '') for w in tokens]
    # get hashtags
    hashtags = [token for token in tokens if '#' in token]
    # get operation hashtags
    hashtags = [hashtag for hashtag in hashtags if '#op' == hashtag[:3]]
    return hashtags


def read_from_env_file():
    """Function to read from env file

    Returns:
        dict -- env variables from file
    """

    with open('../.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('='))
            for line in fh.readlines()
            if not line.startswith('#')
        )

    return vars_dict
