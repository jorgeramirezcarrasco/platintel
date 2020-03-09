import csv
import sys
import time
import requests
from bs4 import BeautifulSoup
import json
import re
from rotate_ip import make_request
import math


def getHashtagTimeline(twitter_hashtag):
    # min_timestamp= datetime.datetime.now() + datetime.timedelta(-30)
    # min_timestamp=min_timestamp.timestamp()
    # print(min_timestamp)
    f = csv.writer(open("tweets"+twitter_hashtag+".csv", "a"))
    u = csv.writer(open("users"+twitter_hashtag+".csv", "a"))

    proxy_active = 0
    proxy_active_value = ""

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
        ('composed_count', '0'),
        ('include_available_features', '1'),
        ('include_entities', '1'),
        ('include_new_items_bar', 'true'),
        ('interval', '30000'),
        ('latent_count', '0'),
        ('reset_error_state', 'false'),
    )

    url = 'https://twitter.com/i/search/timeline'
    proxy_active, proxy_active_value, page = make_request(
        proxy_active, proxy_active_value, url, headers, params)

    data = json.loads(page.content)
    min_position = math.inf
    max_position = 0
    soup = BeautifulSoup(data["items_html"], "lxml")
    retweets = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet ")
    retweetscards = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards has-content ")
    retweets = retweets+retweetscards
    tweets = soup.findAll("div", class_="original-tweet")
    tweetscards = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards  has-content ")
    tweets = tweets + tweetscards
    item_tweet = {}
    for tweet in tweets:
        soup_tweet = BeautifulSoup(str(tweet), "lxml")
        if(soup_tweet.find("span", class_="_timestamp")):
            item_tweet["timestamp"] = soup_tweet.find(
                "span", class_="_timestamp")["data-time"]
        last_tweet_timestamp = float(item_tweet["timestamp"])
        # if(last_tweet_timestamp>min_timestamp):
        if(1):
            item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
            item_tweet["username"] = soup_tweet.find(
                "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
            item_tweet["id_user"] = soup_tweet.div["data-user-id"]
            item_tweet["link_tweet"] = "twitter.com" + \
                soup_tweet.div["data-permalink-path"]
            item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
                "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
            item_tweet["img_user"] = soup_tweet.find(
                "img", class_="avatar js-action-profile-avatar")["src"]
            user_write = (item_tweet["username"], item_tweet["id_user"],
                          item_tweet["img_user"], item_tweet["link_user"])
            u.writerow(user_write)

            item_tweet["text"] = soup_tweet.find(
                "p", class_="TweetTextSize js-tweet-text tweet-text")
            if(item_tweet["text"] is None):
                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
            else:
                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text").text
            tags_tweet = soup_tweet.find("div", class_="media-tags-container")
            if(tags_tweet):
                tags = tags_tweet.findAll("a", class_="js-user-profile-link")
                for tag in tags:
                    if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                        item_tweet["id_user_tag"] = tag["data-user-id"]
                        item_tweet["username_tag"] = tag["href"][1:]
            p_text = soup_tweet.find(
                "p", class_="TweetTextSize js-tweet-text tweet-text")
            if(p_text is None):
                p_text = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
            links_text = p_text.findAll("a")
            for link in links_text:
                if("hashtag_click" in str(link)):
                    item_tweet["hashtag"] = link.text[1:]
                if("mentioned" in str(link)):
                    item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
                    item_tweet["username_mention"] = link.text[1:]
            stats = soup_tweet.find(
                "div", "ProfileTweet-actionCountList u-hiddenVisually")
            counts = stats.findAll("span", class_="ProfileTweet-actionCount")
            item_tweet["replies_count"] = 0
            item_tweet["retweets_count"] = 0
            item_tweet["likes_count"] = 0
            for count in counts:
                if("respuesta" in count.text):
                    item_tweet["replies_count"] = count["data-tweet-stat-count"]
                if("retweet" in count.text):
                    item_tweet["retweets_count"] = count["data-tweet-stat-count"]
                if("gusta" in count.text):
                    item_tweet["likes_count"] = count["data-tweet-stat-count"]

            tweet_write = (item_tweet["id_tweet"], item_tweet["id_user"], item_tweet["username"], item_tweet["link_tweet"],
                           item_tweet["timestamp"], item_tweet["text"], item_tweet["replies_count"], item_tweet["retweets_count"], item_tweet["likes_count"])
            f.writerow(tweet_write)
    for tweet in retweets:
        soup_tweet = BeautifulSoup(str(tweet), "lxml")
        if(soup_tweet.find("span", class_="_timestamp")):
            item_tweet["timestamp"] = soup_tweet.find(
                "span", class_="_timestamp")["data-time"]
        elif(soup_tweet.find("span", class_="_timestamp js-short-timestamp js-relative-timestamp")):
            item_tweet["timestamp"] = soup_tweet.find(
                "span", class_="_timestamp js-short-timestamp js-relative-timestamp")["data-time"]
        last_tweet_timestamp = float(item_tweet["timestamp"])
        # if(last_tweet_timestamp>min_timestamp):
        if(1):
            item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
            item_tweet["username"] = soup_tweet.find(
                "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
            item_tweet["id_user"] = soup_tweet.div["data-user-id"]
            item_tweet["link_tweet"] = "twitter.com" + \
                soup_tweet.div["data-permalink-path"]
            item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
                "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
            item_tweet["img_user"] = soup_tweet.find(
                "img", class_="avatar js-action-profile-avatar")["src"]
            user_write = (item_tweet["username"], item_tweet["id_user"],
                          item_tweet["img_user"], item_tweet["link_user"])
            u.writerow(user_write)
            retweet_write = (twitter_hashtag, item_tweet['id_tweet'])
            f.writerow(retweet_write)

            item_tweet["text"] = soup_tweet.find(
                "p", class_="TweetTextSize js-tweet-text tweet-text")
            if(item_tweet["text"] is None):
                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
            else:
                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text").text
            tags_tweet = soup_tweet.find("div", class_="media-tags-container")
            if(tags_tweet):
                tags = tags_tweet.findAll("a", class_="js-user-profile-link")
                for tag in tags:
                    if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                        item_tweet["id_user_tag"] = tag["data-user-id"]
                        item_tweet["username_tag"] = tag["href"][1:]
            p_text = soup_tweet.find(
                "p", class_="TweetTextSize js-tweet-text tweet-text")
            if(p_text is None):
                p_text = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
            links_text = p_text.findAll("a")
            for link in links_text:
                if("hashtag_click" in str(link)):
                    item_tweet["hashtag"] = link.text[1:]
                if("mentioned" in str(link)):
                    item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
                    item_tweet["username_mention"] = link.text[1:]
            stats = soup_tweet.find(
                "div", "ProfileTweet-actionCountList u-hiddenVisually")
            counts = stats.findAll("span", class_="ProfileTweet-actionCount")
            item_tweet["replies_count"] = 0
            item_tweet["retweets_count"] = 0
            item_tweet["likes_count"] = 0
            for count in counts:
                if("respuesta" in count.text):
                    item_tweet["replies_count"] = count["data-tweet-stat-count"]
                if("retweet" in count.text):
                    item_tweet["retweets_count"] = count["data-tweet-stat-count"]
                if("gusta" in count.text):
                    item_tweet["likes_count"] = count["data-tweet-stat-count"]

            tweet_write = (item_tweet["id_tweet"], item_tweet["id_user"], item_tweet["username"], item_tweet["link_tweet"],
                           item_tweet["timestamp"], item_tweet["text"], item_tweet["replies_count"], item_tweet["retweets_count"], item_tweet["likes_count"])
            f.writerow(tweet_write)
    has_more_items = True
    last_tweet_id = 0
    count_tweets = 20

    # while (has_more_items):
    while ((has_more_items) & (count_tweets < 1000)):
        print(count_tweets)
    # while ((has_more_items) & (last_tweet_timestamp>min_timestamp)):
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

        soup = BeautifulSoup(data["items_html"], "lxml")
        retweets = soup.findAll(
            "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet tweet-has-context ")
        retweetscards = soup.findAll(
            "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet tweet-has-context has-cards has-content ")
        retweets = retweets+retweetscards
        tweets = soup.findAll("div", class_="original-tweet")
        tweetscards = soup.findAll(
            "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards cards-forward ")
        tweets = tweets + tweetscards
        item_tweet = {}
        for tweet in tweets:
            soup_tweet = BeautifulSoup(str(tweet), "lxml")
            if(soup_tweet.find("span", class_="_timestamp")):
                item_tweet["timestamp"] = soup_tweet.find(
                    "span", class_="_timestamp")["data-time"]
            elif(soup_tweet.find("span", class_="_timestamp js-short-timestamp js-relative-timestamp")):
                item_tweet["timestamp"] = soup_tweet.find(
                    "span", class_="_timestamp js-short-timestamp js-relative-timestamp")["data-time"]
            last_tweet_timestamp = float(item_tweet["timestamp"])
            # if(last_tweet_timestamp>min_timestamp):
            if(1):
                item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
                item_tweet["username"] = soup_tweet.find(
                    "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
                item_tweet["id_user"] = soup_tweet.div["data-user-id"]
                item_tweet["link_tweet"] = "twitter.com" + \
                    soup_tweet.div["data-permalink-path"]
                item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
                    "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
                item_tweet["img_user"] = soup_tweet.find(
                    "img", class_="avatar js-action-profile-avatar")["src"]
                user_write = (item_tweet["username"], item_tweet["id_user"],
                              item_tweet["img_user"], item_tweet["link_user"])
                u.writerow(user_write)

                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text")
                if(item_tweet["text"] is None):
                    item_tweet["text"] = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
                else:
                    item_tweet["text"] = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text").text
                tags_tweet = soup_tweet.find(
                    "div", class_="media-tags-container")
                if(tags_tweet):
                    tags = tags_tweet.findAll(
                        "a", class_="js-user-profile-link")
                    for tag in tags:
                        if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                            item_tweet["id_user_tag"] = tag["data-user-id"]
                            item_tweet["username_tag"] = tag["href"][1:]
                p_text = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text")
                if(p_text is None):
                    p_text = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
                links_text = p_text.findAll("a")
                for link in links_text:
                    if("hashtag_click" in str(link)):
                        item_tweet["hashtag"] = link.text[1:]
                    if("mentioned" in str(link)):
                        item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
                        item_tweet["username_mention"] = link.text[1:]
                stats = soup_tweet.find(
                    "div", "ProfileTweet-actionCountList u-hiddenVisually")
                counts = stats.findAll(
                    "span", class_="ProfileTweet-actionCount")
                item_tweet["replies_count"] = 0
                item_tweet["retweets_count"] = 0
                item_tweet["likes_count"] = 0
                for count in counts:
                    if("respuesta" in count.text):
                        item_tweet["replies_count"] = count["data-tweet-stat-count"]
                    if("retweet" in count.text):
                        item_tweet["retweets_count"] = count["data-tweet-stat-count"]
                    if("gusta" in count.text):
                        item_tweet["likes_count"] = count["data-tweet-stat-count"]

                tweet_write = (item_tweet["id_tweet"], item_tweet["id_user"], item_tweet["username"], item_tweet["link_tweet"],
                               item_tweet["timestamp"], item_tweet["text"], item_tweet["replies_count"], item_tweet["retweets_count"], item_tweet["likes_count"])
                f.writerow(tweet_write)
        for tweet in retweets:
            soup_tweet = BeautifulSoup(str(tweet), "lxml")
            if(soup_tweet.find("span", class_="_timestamp js-short-timestamp ")):
                item_tweet["timestamp"] = soup_tweet.find(
                    "span", class_="_timestamp")["data-time"]
            elif(soup_tweet.find("span", class_="_timestamp")):
                item_tweet["timestamp"] = soup_tweet.find(
                    "span", class_="_timestamp js-short-timestamp js-relative-timestamp")["data-time"]
            last_tweet_timestamp = float(item_tweet["timestamp"])
            # if(last_tweet_timestamp>min_timestamp):
            if(1):
                item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
                item_tweet["username"] = soup_tweet.find(
                    "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
                item_tweet["id_user"] = soup_tweet.div["data-user-id"]
                item_tweet["link_tweet"] = "twitter.com" + \
                    soup_tweet.div["data-permalink-path"]
                item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
                    "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
                item_tweet["img_user"] = soup_tweet.find(
                    "img", class_="avatar js-action-profile-avatar")["src"]
                user_write = (item_tweet["username"], item_tweet["id_user"],
                              item_tweet["img_user"], item_tweet["link_user"])
                u.writerow(user_write)

                item_tweet["text"] = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text")
                if(item_tweet["text"] is None):
                    item_tweet["text"] = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
                else:
                    item_tweet["text"] = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text").text
                tags_tweet = soup_tweet.find(
                    "div", class_="media-tags-container")
                if(tags_tweet):
                    tags = tags_tweet.findAll(
                        "a", class_="js-user-profile-link")
                    for tag in tags:
                        if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                            item_tweet["id_user_tag"] = tag["data-user-id"]
                            item_tweet["username_tag"] = tag["href"][1:]
                p_text = soup_tweet.find(
                    "p", class_="TweetTextSize js-tweet-text tweet-text")
                if(p_text is None):
                    p_text = soup_tweet.find(
                        "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
                links_text = p_text.findAll("a")
                for link in links_text:
                    if("hashtag_click" in str(link)):
                        item_tweet["hashtag"] = link.text[1:]
                    if("mentioned" in str(link)):
                        item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
                        item_tweet["username_mention"] = link.text[1:]
                stats = soup_tweet.find(
                    "div", "ProfileTweet-actionCountList u-hiddenVisually")
                counts = stats.findAll(
                    "span", class_="ProfileTweet-actionCount")
                item_tweet["replies_count"] = 0
                item_tweet["retweets_count"] = 0
                item_tweet["likes_count"] = 0
                for count in counts:
                    if("respuesta" in count.text):
                        item_tweet["replies_count"] = count["data-tweet-stat-count"]
                    if("retweet" in count.text):
                        item_tweet["retweets_count"] = count["data-tweet-stat-count"]
                    if("gusta" in count.text):
                        item_tweet["likes_count"] = count["data-tweet-stat-count"]
                tweet_write = (item_tweet["id_tweet"], item_tweet["id_user"], item_tweet["username"], item_tweet["link_tweet"],
                               item_tweet["timestamp"], item_tweet["text"], item_tweet["replies_count"], item_tweet["retweets_count"], item_tweet["likes_count"])
                f.writerow(tweet_write)
        count_tweets = count_tweets+20
        if "id_tweet" in item_tweet:
            if last_tweet_id == item_tweet["id_tweet"]:
                has_more_items = False
            last_tweet_id = item_tweet["id_tweet"]
        else:
            has_more_items = False

        time.sleep(0.1)
