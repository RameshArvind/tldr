import re
import datetime
import csv

def extract(s, vodid):
    matches = re.search("[[](.*)[,]\s(.*)\s([AP]M)]\s[<](.*)[>]\s(.*)", s)
    if( not matches):
        return []
    ts = matches.group(1) + "-" + matches.group(2) + "-" + matches.group(3)
    return [int(datetime.datetime.strptime(ts, "%d/%m/%y-%I:%M:%S-%p").strftime("%s")) , matches.group(4), matches.group(5), vodid]

def read_vod(vod_data):
  with open(vod_data["chatlog"], "r") as f:
    lines = f.readlines()
  lines = [x.strip() for x in lines]
  lines = list(filter(lambda y: len(y) > 0, map(lambda x: extract(x, vod_data["vodid"]), lines)))
  return [lines, vod_data["duration"]]

def get_top_model_groups_by_count(model_group, count):
    return model_group[:count]

def compile_highlights(top_model_groups, interval):
    return [model_group[0] for model_group in top_model_groups]

dataset = [
    {"vodid": 111111, "chatlog": "../tldr/lolchat.txt", "clips": [[1, 10], [30, 40]], "duration" : 60*60*10},
    {"vodid": 22222, "chatlog": "../tldr/cschat.txt", "clips": [[30, 50], [65, 75]], "duration" : 60*60*1}
]


all_vod_messages = [read_vod(x) for x in dataset]
INTERVAL = 7
HIGHLIGHT_COUNT = 10
OVERLAP_RATIO = 0.1

for vod_messages in all_vod_messages:
    start_time = vod_messages[0][0][0]
    model_groups = {(x, x+INTERVAL) : 0 for x in range(0, vod_messages[1])}
    for message in vod_messages[0]:
        bucket = (message[0]-start_time)

        for index in range(bucket - INTERVAL, bucket + INTERVAL + 1):
            if((index, index + INTERVAL) in model_groups):
                model_groups[(index, index + INTERVAL)] += 1

    di = list(model_groups.iteritems())
    for epoch in range(3):
        i = 0
        while(i<len(di)-1):
            cand1 = di[i]
            cand2 = di[i+1]
            set1 = set(range(cand1[0][0], cand1[0][1]))
            inter = set1.intersection(set(range(cand2[0][1], cand2[0][0])))
            print(inter)
            if(len(inter) > OVERLAP_RATIO * (cand1[0][1] - cand1[0][0])):
                cand1_count = di[i][1] #/ (cand1[0][1] - cand1[0][0])
                cand2_count = di[i+1][1] #/ (cand2[0][1] - cand2[0][0])
                if(abs(cand1_count - cand2_count) < 10):
                    di = di[:i] + [(cand1[0][0], cand2[0][1]), int((cand1_count + cand2_count)/2)]
                elif cand1_count > cand2_count :
                    di = di[:i+1] + di[i+2:]
                else:
                    di = di[:i] + di[i+1:]
            else:
                i += 1
    model_groups = di    
    print(sorted(model_groups, key = lambda x: x[1], reverse = True)[:20])
    sorted_model_groups = sorted(model_groups.iteritems(), key = lambda (bucket, messages) : len(messages), reverse = True)

    top_model_groups = get_top_model_groups_by_count(sorted_model_groups, HIGHLIGHT_COUNT)

    highlights = compile_highlights(top_model_groups, INTERVAL)

    print([str(datetime.timedelta(seconds = highlight[0])) for highlight in highlights])