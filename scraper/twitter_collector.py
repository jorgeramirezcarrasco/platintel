# -*- encoding: utf-8 -*-
import csv
import datetime
import functools
import json
import os
import re
import sys
import time

import requests

from twitter_hashtag_collector import getHashtagTimeline
from twitter_timeline_collector import getTimelineUser

if(len(sys.argv) != 1):
    file = open("tweets"+sys.argv[1]+".csv", "w")
    writer = csv.writer(file)
    writer.writerow(["id_tweet", "id_user", "user", "link_tweet", "timestamp",
                     "text", "replies_count", "retweets_count", "likes_count"])
    file.close()
    file = open("users"+sys.argv[1]+".csv", "w")
    writer = csv.writer(file)
    writer.writerow(["username", "id_user", "img_user", "link_user"])
    file.close()

    getHashtagTimeline(sys.argv[1])

    with open('users'+sys.argv[1]+'.csv', newline='') as File:
        with open('users.csv', 'w', newline='') as outFile:
            reader = csv.reader(File)
            for row in reader:
                if(('anon' in row[0].lower()) or ('lulz' in row[0].lower()) or ('ghost' in row[0].lower()) or ('legion' in row[0].lower()) or ('hacker' in row[0].lower()) or ('sechack' in row[0].lower()) or ('cyberteam' in row[0].lower())):
                    writer = csv.writer(outFile, delimiter=',')
                    writer.writerow([row[0][1:]])

    with open('users.csv', 'r') as in_file, open('usersanon.csv', 'w') as out_file:
        seen = set()  # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen:
                continue  # skip duplicate

            seen.add(line)
            out_file.write(line)
    os.system("rm users.csv")

    with open('usersanon.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            getTimelineUser(str(row[0]))
            time.sleep(2)
    path = './'
    os.system("mkdir 1_output")
    files = os.listdir(path)
    tweets_files = []

    for name in files:
        if(name.startswith('timeline')):
            tweets_files.append(name)

    fout = open("./1_output/tweets.csv", "a")
    # first file:
    for line in open(path+tweets_files[0]):
        fout.write(line)
    # now the rest:
    for num in range(1, len(tweets_files)):
        f = open(path+tweets_files[num], "r+")
        next(f)
        for line in f:
            fout.write(line)
        f.close()
    fout.close()
    for file in tweets_files:
        os.system("rm "+file)
    os.system("mv ./1_output/tweets.csv "+str(sys.argv[1])+".csv")
    os.system("rm usersanon.csv")
    os.system("rm -r ./1_output")


else:
    print("Incorrect use, please write a Timeline. Example 'python3 twitter_collector.py duomo'")
