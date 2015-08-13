#!/usr/bin/env python

from py411 import Py411
#from py411_config import config
from samples.py411_config import config

import pprint
import traceback

pp = pprint.PrettyPrinter(indent=4)

api = Py411()
username = config['username']
password = config['password']
print("Login with %r %r" % (username, '*'*len(password)))
response = api.login(username, password)
pp.pprint(response)
uid = response['uid']
token = response['token']

print("""uid: %s
token: %s
""" % (uid, token))

print("users_profile")
response = api.users_profile(uid)
pp.pprint(response)

print("categories_tree")
response = api.categories_tree()
pp.pprint(response)

print("terms_tree")
response = api.terms_tree()
pp.pprint(response)

print("torrents_top")
#response = api._get('/torrents/top/today')
response = api.torrents_top('today')
pp.pprint(response)

print("torrents_search")
query = 'tpb'
response = api.torrents_search(query, limit=2)
pp.pprint(response)
#import pandas as pd
#df = pd.DataFrame(response['torrents'])

id = response['torrents'][0]['id']

print("torrents_download")
filename = "%s.torrent" % id
print("Download and write %s" % filename)
response = api.torrents_download(id)
with open(filename, 'wb') as f:
    f.write(response)

print("bookmarks")
response = api.bookmarks()
print(response)

print("bookmarks_save")
try:
    response = api.bookmarks_save(id)
except:
    print(traceback.format_exc())
print(response)

print("bookmarks_delete")
response = api.bookmarks_delete(id)
print(response)

print("bookmarks")
response = api.bookmarks()
print(response)

print("End")
