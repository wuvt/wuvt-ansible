#!/usr/bin/python

import datetime
import requests
import sys

if sys.version_info[0] >= 3:
    import urllib.parse as urllib
else:
    import urllib

endpoint = "http://localhost:9200"
prune_types = ['cron', 'icecast', 'nginx', 'ntp', 'postfix', 'selinux', 'syslog', 'uwsgi', 'yum']
prune_start = datetime.datetime.utcnow() - datetime.timedelta(days=60)

r = requests.get('{0}/_cat/indices'.format(endpoint))
for line in r.text.splitlines():
    data = line.split(' ')
    if len(data) > 10:
        index = data[2]
        indexd = index.split('-')
        if indexd[0] in prune_types:
            d = datetime.datetime.strptime(indexd[1], "%Y.%m.%d")
            if d < prune_start:
                r2 = requests.delete('{0}/{1}'.format(
                    endpoint, urllib.quote(index)))
                print(index, r2.json())
