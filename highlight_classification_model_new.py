import re
import datetime
import csv
import json

def extract(s, vodid):
    matches = re.search("[[](.*)[,]\s(.*)\s([AP]M)]\s[<](.*)[>]\s(.*)", s)
    if( not matches):
        return []
    ts = matches.group(1) + "-" + matches.group(2) + "-" + matches.group(3)
    return [int(datetime.datetime.strptime(ts, "%m/%d/%y-%I:%M:%S-%p").strftime("%s")) , matches.group(4), matches.group(5), vodid]

def read_vod(vod_data):
  with open(vod_data["chatlog"], "r") as f:
    lines = f.readlines()
  lines = [x.strip() for x in lines]
  lines = list(filter(lambda y: len(y) > 0, map(lambda x: extract(x, vod_data["vodid"]), lines)))
  return [lines, vod_data["duration"], vod_data["vodid"]]

def get_top_model_groups_by_count(model_group, count):
    return model_group[:count]

def compile_highlights(top_model_groups, interval):
    return [model_group[0] for model_group in top_model_groups]

dataset = [
    {
      "chatlog": "tldr/extract-twitch-shit/chats/90000322.chat",
      "duration": 37012,
      "vodid": "90000322",
      "clips": [[27702, 27734]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/161345632.chat",
      "duration": 23585,
      "vodid": "161345632",
      "clips": [[19368, 19398]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/162406490.chat",
      "duration": 43925,
      "vodid": "162406490",
      "clips": [[19344, 19380]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/324500058.chat",
      "duration": 47482,
      "vodid": "324500058",
      "clips": [[17335, 17352]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/337536082.chat",
      "duration": 39658,
      "vodid": "337536082",
      "clips": [[10723, 10733]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/136911382.chat",
      "duration": 36324,
      "vodid": "136911382",
      "clips": [[31251, 31286]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/157526253.chat",
      "duration": 25688,
      "vodid": "157526253",
      "clips": [[24845, 24875]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/185013716.chat",
      "duration": 42538,
      "vodid": "185013716",
      "clips": [[34905, 34932]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/322005220.chat",
      "duration": 25177,
      "vodid": "322005220",
      "clips": [[24683, 24730]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/138023741.chat",
      "duration": 17455,
      "vodid": "138023741",
      "clips": [[7613, 7645]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/252765634.chat",
      "duration": 46425,
      "vodid": "252765634",
      "clips": [[32708, 32738]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/332440904.chat",
      "duration": 39731,
      "vodid": "332440904",
      "clips": [[24572, 24601]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/333414544.chat",
      "duration": 33713,
      "vodid": "333414544",
      "clips": [[27706, 27732]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/140716170.chat",
      "duration": 26662,
      "vodid": "140716170",
      "clips": [[11657, 11676]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/149340095.chat",
      "duration": 35440,
      "vodid": "149340095",
      "clips": [[27513, 27572]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/157767329.chat",
      "duration": 23152,
      "vodid": "157767329",
      "clips": [[13335, 13365]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/84774514.chat",
      "duration": 14731,
      "vodid": "84774514",
      "clips": [[13087, 13120]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/90695672.chat",
      "duration": 26063,
      "vodid": "90695672",
      "clips": [[13559, 13587]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/171190663.chat",
      "duration": 3428,
      "vodid": "171190663",
      "clips": [[34303, 34333]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/178801728.chat",
      "duration": 31647,
      "vodid": "178801728",
      "clips": [[23422, 23448]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/322005066.chat",
      "duration": 91016,
      "vodid": "322005066",
      "clips": [[21776, 21806]]
    },
    {
      "chatlog": "tldr/extract-twitch-shit/chats/103229429.chat",
      "duration": 50400,
      "vodid": "103229429",
      "clips": [[21776, 21806]]
    }
]


all_vod_messages = [read_vod(x) for x in dataset]
INTERVAL = 30
HIGHLIGHT_COUNT = 10
OVERLAP_RATIO = 0.2
db = {}
for vod_messages in all_vod_messages:
    start_time = vod_messages[0][0][0]
    model_groups = {(x, x+INTERVAL) : 0 for x in range(0, vod_messages[1])}
    for message in vod_messages[0]:
        bucket = (message[0]-start_time)

        for index in range(bucket - INTERVAL, bucket + INTERVAL + 1):
            if((index, index + INTERVAL) in model_groups):
                model_groups[(index, index + INTERVAL)] += 1

    di = sorted(list(model_groups.iteritems()), key = lambda x: x[0][0])
    i = 0
    while(i<len(di)-1):
        cand1 = di[i]
        cand2 = di[i+1]
        set1 = set(range(cand1[0][0], cand1[0][1]))
        inter = set1.intersection(set(range(cand2[0][0], cand2[0][1])))
        if(len(inter) >= OVERLAP_RATIO * len(set1)):
            cand1_count = di[i][1] #/ (cand1[0][1] - cand1[0][0])
            cand2_count = di[i+1][1] #/ (cand2[0][1] - cand2[0][0])
            if cand1_count > cand2_count :
                di = di[:i+1] + di[i+2:]
            else:
                di = di[:i] + di[i+1:]
        else:
            i += 1
    model_groups = di    
    sorted_model_groups = sorted(model_groups, key = lambda x: x[1], reverse = True)[:20]

    top_model_groups = get_top_model_groups_by_count(sorted_model_groups, HIGHLIGHT_COUNT)

    highlights = compile_highlights(top_model_groups, INTERVAL)

    db[vod_messages[-1]] = {"data" : highlights}

print(db)
with open("db3.json", "w") as r:
    json.dump(db, r)