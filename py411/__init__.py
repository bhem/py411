#!/usr/bin/env python

import requests
import six

"""
Py411 is a Python library for API
https://api.t411.io/
"""

URL_BASE = 'https://api.t411.io'

try:
    import pandas as pd
    _PANDAS_INSTALLED = True
except ImportError:
    _PANDAS_INSTALLED = False

class Py411(object):
    def __init__(self, url_base=URL_BASE):
        self._url_base = url_base
        self._session = requests
        self.token = None
        self.to_dataframe = True
        print('Init API Client for %r' % self._url_base)

    def login(self, username, password):
        endpoint = '/auth'
        url = self._url(endpoint)
        parsed_response = self._post(endpoint, binary=False, username=username, password=password)
        self.uid = parsed_response['uid']
        self.token = parsed_response['token']
        return parsed_response

    def _headers(self):
        if self.token is None:
            return {}
        else:
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
        headers = self._headers()
        response = self._session.get(url, params=kwargs, headers=headers)
        parsed_response = self._parse_response(response, binary=binary)
        return parsed_response

    def _post(self, endpoint, binary=False, **kwargs):
        url = self._url(endpoint)
        headers = self._headers()
        response = self._session.post(url, data=kwargs, headers=headers)
        parsed_response = self._parse_response(response, binary=binary)
        return parsed_response

    def _delete(self, endpoint, binary=False, **kwargs):
        url = self._url(endpoint)
        response = self._session.delete(url, data=kwargs, headers=self._headers())
        parsed_response = self._parse_response(response, binary=False)
        return parsed_response

    def users_profile(self, id, **kwargs):
        endpoint = '/users/profile/%s' % id
        response = self._get(endpoint, binary=False, **kwargs)
        return response

    def categories_tree(self, **kwargs):
        endpoint = '/categories/tree'
        response = self._get(endpoint, binary=False, **kwargs)
        return response

    def terms_tree(self, **kwargs):
        endpoint = '/terms/tree'
        response = self._get(endpoint, binary=False, **kwargs)
        return response

    def torrents_search(self, query, **kwargs):
        endpoint = '/torrents/search/%s' % query
        response = self._get(endpoint, binary=False, **kwargs)
        if self._return_dataframe:
            key = "torrents"
            try:
                response[key] = pd.DataFrame(response[key])
            except:
                columns = ['added', 'category', 'categoryimage', 'categoryname', 
                    'comments', 'id', 'isVerified', 'leechers', 'name', 'owner', 
                    'privacy', 'rewritename', 'seeders', 'size', 'times_completed', 
                    'username']
                response[key] = pd.DataFrame(columns=columns)

        return response

    def torrents_download(self, id, **kwargs):
        endpoint = '/torrents/download/%s' % id
        response = self._get(endpoint, binary=True, **kwargs)
        return response

    def torrents_top(self, t, **kwargs):
        if isinstance(t, six.string_types):
            t = t.lower()
        endpoint = '/torrents/top/%s' % t
        response = self._get(endpoint, binary=False, **kwargs)
        if self._return_dataframe:
            response = pd.DataFrame(response)
        return response

    def bookmarks(self, **kwargs):
        endpoint = '/bookmarks'
        response = self._get(endpoint, binary=False, **kwargs)
        return response        

    def bookmarks_save(self, torrent_id, **kwargs):
        endpoint = '/bookmarks/save/%s' % torrent_id
        response = self._post(endpoint, data=kwargs)
        return response

    def bookmarks_delete(self, torrent_id, **kwargs):
        if hasattr(torrent_id, '__iter__'):
            if not isinstance(torrent_id, six.string_types):
                torrent_id = ",".join(torrent_id)
        endpoint = '/bookmarks/delete/%s' % torrent_id
        response = self._delete(endpoint, data=kwargs)
        return response

    @property
    def _return_dataframe(self):
        return _PANDAS_INSTALLED and self.to_dataframe

    def get(self, partial_response, idx, col):
        if not self._return_dataframe:
            return partial_response[idx][col]
        else:
            return partial_response.loc[idx, col]
