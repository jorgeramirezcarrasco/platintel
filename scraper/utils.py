import os
import string
from itertools import cycle
from re import findall
import json

import nltk
import numpy as np
import pandas as pd
import requests
from nltk.corpus import stopwords


def clean_text(x):
    """Function to clean text from tweets

    Arguments:
        x {str} -- input text

    Returns:
        str -- text cleaned
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


def get_hashtags_operations(x):
    """Function to obtain hashtags from a tweet

    Arguments:
        x {str} -- input tweet

    Returns:
        [list] -- list of hashtags extracted
    """
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


def get_proxies():
    """Function to obtain available proxies from sslproxies

    Returns:
        [list] -- list of proxies
    """
    r = requests.get('https://www.sslproxies.org/')
    matches = findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
    revised = [m.replace('<td>', '') for m in matches]
    proxies = [s[:-5].replace('</td>', ':') for s in revised]
    return proxies


def make_request(proxy_active, proxy_active_value, url, headers, params):
    """Function to make a request through a proxy

    Arguments:
        proxy_active {int} -- boolean about the active proxy
        proxy_active_value {str} -- active proxy
        url {str} -- url to make the request
        headers {dict} -- headers to send with the request
        params {dict} -- params to send with the request

    Returns:
        [int, str, dict] -- proxy information and result of the request
    """
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(100):
        if proxy_active != 1:
            proxy_active_value = next(proxy_pool)
        try:
            response = requests.get('https://httpbin.org/ip', timeout=3.0, proxies={
                                    "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
            page = requests.get(url, headers=headers, params=params, proxies={
                                "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
            proxy_active = 1
            if page.status_code == 200:
                return proxy_active, proxy_active_value, page
        except Exception as e:
            proxy_active = 0
            continue
    return proxy_active, proxy_active_value, "Error"


def create_dict_from_structure(key):
    """Function to create a dict structure from the template defined in the json

    Arguments:
        key {str} -- key in the json artifact

    Returns:
        dict -- template dict to fill
    """
    with open('../artifacts/scraper_outputs.json') as json_file:
        json_file_item = json.load(json_file)
        dict_struct = {}
        for column in json_file_item[key]:
            dict_struct[column] = []
        return dict_struct


def filter_anon_username(username):
    """Function to filter anonymous user from dict

    Arguments:
        username {str} -- Username to filter

    Returns:
        [int] -- 1 if match the list of terms, else 0
    """
    with open('../artifacts/scraper_anon_filter.json') as json_file:
        json_file_item = json.load(json_file)
        for term in json_file_item["username"]:
            if term.lower() in username.lower():
                return 1
        return 0


def filter_anon_hashtag(hashtag, search_term):
    """Function to filter anonymous hashtag from dict

    Arguments:
        hashtag {str} -- hashtag to filter
        search_term {str} -- initial search term to filter

    Returns:
        [int] -- 1 if match the list of terms, else 0
    """
    with open('../artifacts/scraper_anon_filter.json') as json_file:
        json_file_item = json.load(json_file)
        for term in json_file_item["hashtag"]["exclude"]:
            if term.lower() in hashtag.lower():
                return 0
        for term in json_file_item["hashtag"]["include"]:
            if search_term.lower() in hashtag.lower():
                return 0
            if term.lower() in hashtag.lower():
                return 1

        return 0


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
