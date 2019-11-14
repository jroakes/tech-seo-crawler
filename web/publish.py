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

import argparse
import os
import requests
import json
import base64
import web.auth as auth

class FilePathMissing(Exception):
    '''An exception for a missing or invalid file path.'''
    pass


class Publish:
    def __init__(self, user, org, repo=None):

        # Set required derived variables
        self.owner  = user
        self.org    = org

        if repo:
            self.repo = repo
        else:
            self.repo = self.org + '.github.io'

        self.api_create_url = 'https://api.github.com/user/repos'
        self.api_template_url = 'https://api.github.com/repos/site-template/template/generate'
        self.api_publish_url = 'https://api.github.com/repos/{org}/{repo}/contents/{path}'



    def get_auth_details(self):
        return auth.Authorization(self.owner).get_auth_details()


    def get_sha_blob(self, api_url):
        """
        if the current file exists
            returns the sha blob
        else
            returns None
        """
        r = requests.get(api_url, auth=self.get_auth_details())
        try:
            return r.json()['sha']
        except KeyError:
            return None



    def create_template_repo(self):

        payload = {'name': self.repo,
                   'owner': self.org }

        print(self.api_template_url)

        r = requests.post(self.api_template_url,
                         auth=self.get_auth_details(),
                         data=json.dumps(payload),
                         headers={'Accept': 'application/vnd.github.baptiste-preview+json'}
                         )

        result = r.json()

        return r.status_code, result


    def publish_post(self, fp, path=None):

        if not fp or not isinstance(fp, str) or len(fp) < 1:
            raise FilePathMissing('`fp` is a required argument and should be of type string.')

        title = os.path.basename(fp)
        path = path + '/' + title if path else '_posts/' + title

        api_publish_url = self.api_publish_url.format(org=self.org, repo=self.repo, path=path)


        # Set base64 encoded content of file
        with open(os.path.abspath(fp), encoding="utf-8") as f:
            content_base64 = base64.b64encode(f.read().encode('utf-8'))

        payload = {'content': content_base64.decode('utf-8')}

        sha_blob = self.get_sha_blob(api_publish_url)

        if sha_blob:
            commit_msg = 'ghPublish UPDATE: {}'.format(title)
            payload.update(sha=sha_blob)
            payload.update(message=commit_msg)
        else:
            commit_msg = 'ghPublish ADD: {}'.format(title)
            payload.update(message=commit_msg)

        r = requests.put(api_publish_url,
                         auth=self.get_auth_details(),
                         data=json.dumps(payload))
        try:
            url = r.json()['content']['html_url']
            return r.status_code, url
        except KeyError:
            return r.status_code, None
