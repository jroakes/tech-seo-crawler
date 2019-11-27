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

import re
from urllib.parse import urlparse, urljoin
import hashlib
import pickle
import os

import config as cfg


def get_canonical_url(href, current_url):

    if href:
        href = href.strip()
        o = urlparse(href)
        if not o.hostname:
            tmp = urlparse(current_url)
            domain = '%s://%s' % (tmp.scheme, tmp.hostname)
            href = urljoin(domain, href)
        return href
    return None


def get_hostname(url):
    url = url.strip()
    o = urlparse(url)
    return o.hostname


def get_robots(url):
    tmp = urlparse(url)
    domain = '%s://%s' % (tmp.scheme, tmp.hostname)
    href = urljoin(domain, '/robots.txt')
    return href

def url_hash(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    return hashlib.md5(url).hexdigest()

def abs_src(html, url):
    temp = lambda m: ' src="' + urljoin(url, m.group(1)) + '"'
    html = re.sub(r' src\s*=\s*"([^"]+)"', temp, html)
    return html

class ClassStorage:

    def __init__(self):
        self.path = 'data'

    def load_pickle(self, fn):
        fn = os.path.join(self.path, fn)
        if os.path.exists(fn):
            return pickle.load(open(fn,'rb'))
        else:
            return None

    def save_pickle(self, fn, cls):
        fn = os.path.join(self.path, fn)
        pickle.dump(cls, open(fn,'wb'))
