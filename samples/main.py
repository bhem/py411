#!/usr/bin/env python

from py411 import Py411
from py411_config import config
import pprint

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

response = api.users_profile(uid)
pp.pprint(response)

response = api.categories_tree()
pp.pprint(response)

response = api.terms_tree()
pp.pprint(response)

response = api._get('/torrents/top/today')
pp.pprint(response)

query = 'tpb'
response = api.torrents_search(query, limit=2)
pp.pprint(response)

id = response['torrents'][0]['id']

filename = "%s.torrent" % id
print("Download and write %s" % filename)
response = api.torrents_download(id)
with open(filename, 'wb') as f:
    f.write(response)
