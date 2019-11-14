#! /usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2019 JR Oakes
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWA


# https://github.com/oxalorg/ghPublish
# Contributors:
# Author: Mitesh Shah
#
# License:
# MIT License
# Copyright (c) 2016 Mitesh Shah

import requests
import os
import json
import getpass
from requests.auth import HTTPBasicAuth


class PassPromptAuth(HTTPBasicAuth):
    def __init__(self, username):
        self.username = username
        self.password = getpass.getpass()


class Authorization():
    config_file = os.path.join(os.path.expanduser('~'), '.ghPublish')
    AUTH_URL = 'https://api.github.com/authorizations'

    def __init__(self, user):
        self.user = user.lower()

    def get_auth_details(self):
        return (self.user, self.get_api_token())

    def get_api_token(self):
        try:
            return self._get_config()['tokens'][self.user]
        except KeyError:
            return self._update_config()

    def _get_config(self):
        try:
            if not os.path.exists(self.config_file):
                config = {"tokens": {}, "defaults": {}, "settings": {}}
                with open(self.config_file, 'a') as f:
                    json.dump(config, f)
            else:
                with open(self.config_file) as f:
                    config = json.load(f)
            return config

        except JSONDecodeError:
            raise SystemExit(
                'Your configuration file seems to be broken! JSON cannot be decoded.')
        except IsADirectoryError:
            raise SystemExit(
                "~/.ghPublish must not exist as a directory. Cannot store configuration.")

    def _request_access_token(self):
        note = "ghPublish: Directly publish your blog posts to GitHub Pages from the command line."
        note_url = 'https://github.com/MiteshNinja/ghPublish'
        scopes = ["public_repo"]
        payload = dict(note=note, scopes=scopes, note_url=note_url)
        print("Visit: https://github.com/settings/tokens to manage tokens.\n")
        print("Requesting one-time ACCESS TOKEN for user: " + self.user)
        r = requests.post(self.AUTH_URL,
                          auth=PassPromptAuth(self.user),
                          data=json.dumps(payload))

        rj = r.json()
        if r.status_code == 201:
            return rj['token']
        elif r.status_code == 401 and rj['message'].lower(
        ) == 'bad credentials':
            raise SystemExit('Bad credentials!')
        elif r.status_code == 422 and rj['message'].lower(
        ) == 'validation failed':
            raise SystemExit(
                'Validation has failed!\nThe response received was:\n {}'.format(
                    rj))
        else:
            raise SystemExit(
                'An error has occurred while creating a token!\nThe response received was:\n {}'.format(
                    rj))

    def _update_config(self):
        config = self._get_config()
        token = self._request_access_token()
        config['tokens'][self.user] = token
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        return token


if __name__ == '__main__':
    a = Authorization('jroakes-locomotive')
    print(a.get_auth_details())
