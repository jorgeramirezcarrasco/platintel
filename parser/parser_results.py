import os

import numpy as np
import json
import pandas as pd
import pymongo

from utils import clean_text, get_hashtags_operations, transform_date, read_from_env_file, check_attack, transform_user_rt_to_tweet, transform_text_rt_to_tweet

directory = '../scraper/'
data_files = []
json_file_item = None
with open('../artifacts/anon_dict.json') as json_file:
    json_file_item = json.load(json_file)

analysis = ""
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.csv') & (True == filename.startswith('results_')):
        data_files.append(pd.read_csv(directory+filename))
        analysis = filename.split('.csv')[0]

df = pd.concat(data_files, sort=False)

df['clean_text'] = df['text'].map(lambda x: clean_text(x))

df['date'] = df['timestamp'].apply(lambda x: transform_date(x))
df['year'] = df['date'].apply(lambda x: x.year)
df = df.loc[df['year'] >= df['year'].max(), ]

df['hashtags'] = df['text'].map(lambda x: get_hashtags_operations(x))

terms_attacks = json_file_item["attacks"]

df['attack'] = df['clean_text'].map(lambda x: check_attack(x, terms_attacks))
df['operations'] = df['hashtags'].map(lambda x: True if len(
    [hashtag for hashtag in x if '#op' == hashtag[:3]]) > 0 else False)
df['RT'] = df['clean_text'].map(lambda x: True if 'rt' in x else False)

# Translate RTs to Attacks
df['user'] = df[(df['RT'] == True)]['text'].apply(
    lambda x: transform_user_rt_to_tweet(x))
df['text'] = df[(df['RT'] == True)]['text'].apply(
    lambda x: transform_text_rt_to_tweet(x))
df['RT'] = False
df = df.drop_duplicates(subset=['user', 'text'])

df_top_hashtags = df[(df['operations'] ==
                      True) & (df['RT'] ==
                               False)]['hashtags'].explode().value_counts().to_frame()
hashtags = df_top_hashtags[df_top_hashtags['hashtags'] > 0].to_dict()[
    'hashtags']

dict_hashtags_rel = {}
for hashtag in hashtags.keys():
    df_hashtag = df[df['operations'] == True][['hashtags', 'user']]
    df_hashtag[hashtag] = df_hashtag['hashtags'].apply(
        lambda x: True if hashtag in x else False)
    dict_hashtags_rel[hashtag] = list(
        df_hashtag.loc[df_hashtag[hashtag], 'user'].value_counts().to_frame().index.values)

dict_groups_rel = {}
for group in json_file_item['groups']:
    df_group = df[df['operations'] == True][['user']]
    df_group[group] = df_group['user'].apply(
        lambda x: True if x in json_file_item['groups'][group] else False)
    dict_groups_rel[group] = list(
        df_group.loc[df_group[group], 'user'].value_counts().to_frame().index.values)

dict_output = {}
list_users = []
json_colors_item = None
with open('../artifacts/parser_color_palette.json') as json_file:
    json_colors_item = json.load(json_file)

for index, row in df[(df['attack'] == True) & (df['RT'] == False) & (df['operations'] == True)].iterrows():
    if row['user'] in list_users:
        dict_output[row['user']].append(
            {"id": row['link_tweet'], "name": "Attack", "value": "", "type": json_colors_item["Attack"]})
    else:
        list_users.append(row['user'])
        dict_output[row['user']] = []
        dict_output[row['user']].append(
            {"id": row['link_tweet'], "name": "Attack", "value": "", "type": json_colors_item["Attack"]})

for index, row in df[(df['attack'] == True) & (df['RT'] == True)].iterrows():
    if row['user'] in list_users:
        dict_output[row['user']].append(
            {"id": row['link_tweet'], "name": "RT of Attack", "value": "", "type": json_colors_item["RT of Attack"]})
    else:
        list_users.append(row['user'])
        dict_output[row['user']] = []
        dict_output[row['user']].append(
            {"id": row['link_tweet'], "name": "RT of Attack", "value": "", "type": json_colors_item["RT of Attack"]})

dict_output_formatted = []
for elem in dict_output:
    dict_output_formatted.append({"id": elem, "name": elem, "value": "",
                                  "collapsed": "true", "children": dict_output[elem], "type": json_colors_item["User"]})
for elem in hashtags.keys():
    if len(list(set(dict_output) & set(dict_hashtags_rel[elem]))) > 0:
        dict_output_formatted.append(
            {"id": elem, "name": elem, "value": hashtags[elem], "collapsed": "true", "linkWith": dict_hashtags_rel[elem], "type": json_colors_item["Hashtag"]})

for elem in json_file_item['groups']:
    if len(list(set(dict_output) & set(dict_groups_rel[elem]))) > 0:
        dict_output_formatted.append(
            {"id": elem, "name": elem, "value": "", "collapsed": "true", "linkWith": dict_groups_rel[elem], "type": json_colors_item["Group"]})


# Upload to database
env_vars = read_from_env_file()
myclient = pymongo.MongoClient(env_vars["MONGO_URL"]+"?retryWrites=false")
mydb = myclient["heroku_l7w1n51h"]
mycoll = mydb["analyses"]
analysis_formatted = "#"+analysis.split("_")[1]+"_"+analysis.split("_")[2]
#mycoll.delete_one({"user": "5e519f9c7c213e67373e1f14"})
mydict = {"user": "5e519f9c7c213e67373e1f14",
          "analysis": analysis_formatted, "data": dict_output_formatted}
mycoll.insert_one(mydict)
