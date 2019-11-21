#!/usr/bin/env python
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

import lib
import pandas as pd


class Crawler():

    def __init__(self, config=None):

        self.frontier  = lib.FrontierQueue()
        self.hashtable = lib.HashLookup()
        self.linkgraph = lib.LinkGraph()

        self.known_urls = set()
        self.crawled_urls = set()

        self.doc_index = pd.DataFrame()
        self.term_index = pd.DataFrame()
        self.link_index = pd.DataFrame()
        self.link_text  = {}



    def parse_links(self, links, current_url):
        self.known_urls.update([l['href'] for l in links])

        valid_urls = set()

        for link in links:

            text = str(link['text']).strip()
            rel  = str(link['rel']).strip()
            href = str(link['href']).strip().split('#')[0]

            # Ignore nofollow
            if rel.lower() == 'nofollow':
                continue

            # Anchor text
            if len(text) and len(href):
                if href in self.link_text:
                    self.link_text[href] += [text]
                else:
                    self.link_text[href] = [text]

            self.linkgraph.add_edge(current_url, href)

            if href in self.crawled_urls or href in self.frontier.items:
                continue

            valid_urls.add(href)

        return list(valid_urls)




    def crawl(self, seed):

        self.frontier.enqueue(seed)

        while len(self.frontier):

            # Pull off next url
            nxt = self.frontier.dequeue()
            print("Crawling: {}".format(nxt))

            nxt_data = lib.crawl_url(nxt)

            if nxt_data:
                self.doc_index = self.doc_index.append(nxt_data, ignore_index=True)
                self.crawled_urls.add(nxt)

                if len(nxt_data['links']):
                    valid_urls = self.parse_links(nxt_data['links'], nxt)
                    self.frontier.enqueue(valid_urls)
