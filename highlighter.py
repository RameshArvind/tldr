import re
import datetime

def extract(s):
    matches = re.search("[[](.*)[,]\s(.*)\s([AP]M)]\s[<](.*)[>]\s(.*)", s)
    if( not matches):
        return []
    ts = matches.group(1) + "-" + matches.group(2) + "-" + matches.group(3)
    return [int(datetime.datetime.strptime(ts, "%d/%m/%y-%I:%M:%S-%p").strftime("%s")), ts , matches.group(4), matches.group(5)]
with open("chat1.txt", "r") as f:
    l = f.readlines()

l = [x.strip() for x in l]
l1 = list(filter(lambda y: len(y) > 0, map(lambda x: extract(x), l)))



interval = 10
start = l1[0][0]
print(start)
mg = {}
for e in l1:
   bucket = int((e[0]-start)/interval) 
   t = mg.get(bucket, [])
   t.append(e)
   mg[bucket] = t

for key,value in sorted(mg.iteritems(), key = lambda (k,v) : len(v)):
    print(str(key) + "---" + str(interval*key/60) + "--"+str((interval*key)%60) + "--"+ str(len(value)))
