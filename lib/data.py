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
        if isinstance(item, list):
            _ = [self.items.append(i) for i in item]
        else:
            self.items.append(item)
    def dequeue(self):
        # Pull from beginning
        return self.items.popleft()
    def __len__(self):
        return len(self.items)


class LinkGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def isEmpty(self):
        return not bool(self.nodes) and not bool(self.edges)
    def add_node(self,node):
        if node not in self.nodes:
            self.nodes.append(node)
    def add_edge(self, origin, destination):
        self.add_node(origin)
        self.add_node(destination)
        self.edges.append((origin, destination))
    def get_data(self):
        return self.nodes, self.edges
    def __len__(self):
        return len(self.nodes)


class LinkGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    def isEmpty(self):
        return not bool(self.nodes) and not bool(self.edges)
    def add_node(self,node):
        if node not in self.nodes:
            self.nodes.append(node)
    def add_edge(self, origin, destination):
        self.add_node(origin)
        self.add_node(destination)
        self.edges.append((origin, destination))
    def get_data(self):
        return self.nodes, self.edges
    def __len__(self):
        return len(self.nodes)


class URLLookup:
    def __init__(self, threshold=0.8):
        self.df = pd.DataFrame(columns=['url_hash','url_str','url_canonical']).set_index('url_hash')
    def isEmpty(self):
        return self.df.empty()
    def add_hashed(self, url_str, url_canonical=""):
        hs = url_hash(url_str)
        self.df.loc[hs] = {'url_str':url_str, 'url_canonical': url_canonical}
        return hs
    def get_hash(self, url_str):
        hs = self.df[self.df.url_str == url_str].index
        return hs.item() if len(hs) else None
    def get_url(self, url_hash):
        hs = self.df.loc[url_hash]['url_str']
        return hs or None
    def get_canonical(self, url_hash):
        hs = self.df.loc[url_hash]['url_canonical']
        return hs or None
    def __len__(self):
        return len(self.df)


class HashLookup:
    def __init__(self, threshold=0.8):
        self.df = pd.DataFrame(columns=['url','minhash'])
        self.th = threshold
    def isEmpty(self):
        return self.df.empty()
    def add_hash(self, url, content):
        self.df = self.df.append({'url':url, 'minhash':build_minhash(content).minhash}, ignore_index=True)
    def get_hash(self, url):
        hs = self.df[ self.df.url == url]['minhash']
        return hs.item() if len(hs) else []
    def get_similar(self, content, threshold=None ):
        th = threshold or self.th
        mh = build_minhash(content)
        matches = self.df.minhash.map(lambda x : mh.similarity(x) > th)
        return self.df[matches]['url'].tolist()
    def get_similarity_df(self, content):
        mh = build_minhash(content)
        df_sim = self.df.copy()
        df_sim['sim'] = df_sim.minhash.map(lambda x : mh.similarity(x))
        return df_sim[['url','sim']].sort_values(by='sim', ascending=False)
    def __len__(self):
        return len(self.df)
