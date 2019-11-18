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

import pandas as pd
from collections import deque
from lib import *

class FrontierQueue:
    def __init__(self):
        self.items = deque()
    def isEmpty(self):
        return not bool(self.items)
    def enqueue(self,item):
        # Add to end
        self.items.append(item)
    def dequeue(self):
        # Pull from beginning
        return self.items.popleft()
    def size(self):
        return len(self.items)


class HashLookup:
    def __init__(self, threshold=0.8):
        self.df = pd.DataFrame(columns=['url','minhash'])
        self.th = threshold
    def isEmpty(self):
        return self.df.empty()
    def add_hash(self, url, content):
        self.df = self.df.append({'url':url, 'minhash':build_minhash(content)}, ignore_index=True)
    def get_hash(self, domain, url):
        return self.df[ self.df.url == url]['minhash']
    def get_similar(self, content ):
        mh = build_minhash(content)
        matches = self.df.minhash.map(lambda x : mh.similarity(x) <= self.th)
        self.df[matches]['url'].tolist()

    def __len__(self):
        return len(self.df)
