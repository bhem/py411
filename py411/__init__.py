#!/usr/bin/env python

import requests

"""
Py411 is a Python library for API
https://api.t411.io/
"""

URL_BASE = 'https://api.t411.io'

class Py411(object):
    def __init__(self, url_base=URL_BASE):
        self._url_base = url_base
        self._session = requests
        print('Init API Client for %r' % self._url_base)

    def login(self, username, password):
        endpoint = '/auth'
        url = self._url(endpoint)
        data = {
            'username': username,
            'password': password,
        }
        response = self._session.post(url, data=data)
        parsed_response = self._parse_response(response)
        self.uid = parsed_response['uid']
        self.token = parsed_response['token']
        return parsed_response

    def _headers(self):
        return {"Authorization": self.token}

    def _url(self, endpoint):
        return self._url_base + endpoint

    def _parse_response(self, response, binary=False):
        status_code = response.status_code
        if status_code != 200:
            raise(Exception("HTTP status code is %d - it should be 200"))
        if binary:
            return response.content
        parsed_response = response.json()
        if isinstance(parsed_response, dict):
            if 'error' in parsed_response.keys():
                raise(Exception("Error code %d - %s" % (parsed_response['code'], parsed_response['error'])))
        return parsed_response

    def _get(self, endpoint, binary=False, **kwargs):
        url = self._url(endpoint)
        response = self._session.get(url, params=kwargs, headers=self._headers())
        parsed_response = self._parse_response(response, binary=binary)
        return parsed_response

    def users_profile(self, id, **kwargs):
        endpoint = '/users/profile/%s' % id
        return self._get(endpoint, binary=False, **kwargs)

    def categories_tree(self, **kwargs):
        endpoint = '/categories/tree'
        return self._get(endpoint, binary=False, **kwargs)

    def terms_tree(self, **kwargs):
        endpoint = '/terms/tree'
        return self._get(endpoint, binary=False, **kwargs)

    def torrents_search(self, query, **kwargs):
        endpoint = '/torrents/search/%s' % query
        return self._get(endpoint, binary=False, **kwargs)

    def torrents_download(self, id, **kwargs):
        endpoint = '/torrents/download/%s' % id
        return self._get(endpoint, binary=True, **kwargs)

    def torrents_top(self, t, **kwargs):
        try:
            t = t.lower()
        except:
            pass
        endpoint = '/torrents/top/%s' % t
        return self._get(endpoint, binary=False, **kwargs)

    def bookmarks(self, **kwargs):
        endpoint = '/bookmarks'
        return self._get(endpoint, binary=False, **kwargs)

    def bookmarks_save(self, torrent_id, **kwargs):
        endpoint = '/bookmarks/save/%s' % torrent_id
        url = self._url(endpoint)
        response = self._session.post(url, data=kwargs, headers=self._headers())
        parsed_response = self._parse_response(response, binary=False)
        return parsed_response

    def bookmarks_delete(self, torrent_id, **kwargs):
        endpoint = '/bookmarks/delete/%s' % torrent_id
        url = self._url(endpoint)
        response = self._session.delete(url, data=kwargs, headers=self._headers())
        parsed_response = self._parse_response(response, binary=False)
        return parsed_response
