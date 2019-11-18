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
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pandas


class Frontier:

    def __init__(self):
        self.db = pd.DataFrame(columns=['domain','url',])

    def add_url(self, domain, url, priority):
        self.db.append({'domain':domain, 'url': url.strip(), 'priority': priority, 'crawled':False}, ignore_index=True)

    def get_new(self, domain):
        return self.db[(self.db.crawled == False & self.db.domain == domain)]['url'].tolist()

    def mark_crawled(self, domain, url):
        self.db[(self.db.domain == domain & self.db.url == url)]['crawled'] = True




class search_index:

    def __init__(self):
        self.db = pd.DataFrame(columns=['domain', 'url', 'title', 'description'])

    def add_url(self, domain, url, title, description):
        if self.url_exists(domain, url):
            self.update_existing(domain, url, title, description)
        else:
            self.db.append({'domain':domain, 'url': url 'title': title, 'description':description}, ignore_index=True)

    def url_exists(self, domain, url):
        return self.db[(self.db.domain == domain & self.db.url == url)].empty() == False

    def update_existing(self, domain, url, title, description):
        self.db.loc[(self.db.domain == domain & self.db.url == url), ['title', 'description']] = title, description
