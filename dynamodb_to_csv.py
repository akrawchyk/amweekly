import csv
import json
from datetime import datetime


data = []
with open('data') as f:
    for line in f:
        data.append(json.loads(line))

with open('data.csv', 'w', encoding='utf8') as csvf:
    w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL)
    w.writerow(['id', 'created_at', 'user_name', 'url'])
    for idx,entry in enumerate(data):
        created_at = datetime.fromtimestamp(int(entry['createdAt']['n'])/1000.0)
        user_name = entry['userName']['s']
        url = entry['url']['s']
        w.writerow([idx+1, created_at, user_name, url])
