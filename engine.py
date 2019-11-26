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

from lib import *
import pandas as pd
import streamlit as st

import config as cfg


class Crawler():

    def __init__(self, config=None):

        self.frontier  = FrontierQueue()
        self.linkgraph = LinkGraph()
        self.urllookup = URLLookup()
        self.hashtable  = HashLookup()

        self.known_urls   = set()
        self.crawled_urls = set()

        self.doc_index  = {}
        self.link_text  = {}



    def parse_links(self, links, doc_hash):

        self.known_urls.update([l['href'] for l in links])

        valid_urls = set()

        for link in links:

            text = str(link['text']).strip()
            rel  = str(link['rel']).strip()
            href = str(link['href']).strip().split('#')[0]

            # Ignore nofollow
            if rel.lower() == 'nofollow':
                continue

            if not check_robots_txt(get_robots(href), href):
                continue

            self.update_linktext(href, text)
            self.update_linkgraph(doc_hash, href)

            if href not in self.crawled_urls and href not in self.frontier.items:
                valid_urls.add(href)

        return list(valid_urls)


    def update_linkgraph(self, current, target):
        target = self.urllookup.update_hashed(target)
        self.linkgraph.add_edge(current, target)

    def update_linktext(self, target, text):
        target = self.urllookup.update_hashed(target)
        if len(text) and len(target):
            if target in self.link_text:
                self.link_text[target] += [text]
            else:
                self.link_text[target] = [text]


    def crawl(self, seed):

        self.frontier.enqueue(seed)

        while len(self.frontier):

            # Pull off next url
            url = self.frontier.dequeue()
            status = "Crawling: {}".format(url)
            print(status)
            st.markdown(status)

            url_data = crawl_url(url)

            if url_data and url_data['status'] == 200:

                canonical = url_data['meta']['canonical']

                doc_hash = self.urllookup.update_hashed(url, canonical=canonical)

                doc_data = {'url': url,
                            'domain':url_data['domain'] ,
                            'title': url_data['title'],
                            'description': url_data['meta']['description'],
                            'content': url_data['content'],
                            'html': url_data['html']
                            }

                self.hashtable.add_hash(doc_hash, url_data['content'])

                self.doc_index[doc_hash] = doc_data
                self.crawled_urls.add(url)

                if 'links' in url_data and len(url_data['links']):
                    new_links = url_data['links']
                    valid_urls = self.parse_links(new_links, doc_hash)
                    self.frontier.enqueue(valid_urls)



    def render(self):

        renderer = RenderHTML()

        for doc_hash in self.doc_index:

            status = "Rendering: {}".format(self.urllookup.get_url(doc_hash))
            print(status)
            st.markdown(status)

            doc_data = self.doc_index[doc_hash]

            html_data = renderer.render(html=(doc_data['html']))

            doc_data['title'] = html_data['title'][0]
            doc_data['description'] = html_data['description'][0]

            mh_crawled = build_minhash(doc_data['content'])
            mh_rendered = build_minhash(html_data['content'])

            doc_data['content_sim'] =  mh_crawled.similarity(mh_rendered.minhash)

            doc_data['content'] = html_data['content']

            doc_hash = self.urllookup.update_canonical( doc_hash, canonical=html_data['canonical'][0])

            self.doc_index[doc_hash] = doc_data




class Indexer():

    def __init__(self, crawl_data):

        self.term_index = pd.DataFrame()
        self.bert_term_index = pd.DataFrame()
        self.pr_index   = pd.DataFrame()
        self.doc_index  = pd.DataFrame(crawl_data.doc_index.values(), index=crawl_data.doc_index.keys())
        self.linkgraph  = crawl_data.linkgraph
        self.link_text  = crawl_data.link_text
        self.urllookup  = crawl_data.urllookup
        self.hashtable  = crawl_data.hashtable
        self.bert       = BERT()


    def canonicalize_docs(self, docs):
        content = docs['content'].tolist()
        urlhash = docs.index.tolist()

        canonicals = []

        for u in urlhash:

            options   = [h for h in self.hashtable.get_similar_by_hash(u)]

            if len(options):
                top_pr  = self.pr_index.loc[options].sort_values(by='score', ascending=False).index.tolist()[0]
                center  = len([c for c in set([self.urllookup.get_canonical_hash(u) for u in options]) if c == u]) > 0

                if top_pr == u or center:
                    canonicals.append(u)

            else:
                canonicals.append(u)

        return canonicals


    def build_index(self, i_type=None, title_boost=None):

        title_boost = title_boost or cfg.title_boost
        i_type      = i_type or cfg.i_type

        self.pr_index = build_pagerank_df(list(self.linkgraph.nodes), list(self.linkgraph.edges))

        self.doc_index  = self.doc_index.loc[self.canonicalize_docs(self.doc_index)]

        d_c    = [t.split() for t in self.doc_index['content'].tolist()]
        t_c    = [t.split() for t in self.doc_index['title'].tolist()]

        doc_index  = self.doc_index.index.tolist()

        # Append title, content, and anchor text to doc frequency measurements.
        doc_corpus = [' '.join(t_c[i]*title_boost + d_c[i] + list(set(self.link_text[k]))) for i,k in enumerate(doc_index)]

        if i_type == "bm25":
            self.term_index = get_bm25(doc_corpus, doc_index)
        else:
            self.term_index = get_tfidf(doc_corpus, doc_index)

        self.bert_term_index = get_tfidf_bert(doc_corpus, doc_index)

        self.doc_index = pd.merge(self.doc_index, self.pr_index, left_index=True, right_index=True)


    def build_bert_embeddings_st(self):

        terms = self.bert_term_index.index.tolist()
        len_terms = len(terms)
        perc_complete = 0

        st.markdown('### Building BERT Embeddings')

        my_bar = st.progress(perc_complete)

        for i, t in enumerate(terms):
            self.bert.add_term(t)

            if i % int(len_terms/100) == 0 and i != 0:
                perc_complete += 1
                my_bar.progress(perc_complete)


    def build_bert_embeddings(self):
        from tqdm import tqdm_notebook as tqdm
        for t in tqdm(terms, desc='Building BERT Embeddings'):
            self.bert.add_term(t)

    def search_index(self, search_query, **data):
        return self._search_index(search_query, **data)[0]

    def search_index_st(self, search_query, **data):
        return self._search_index(search_query, **data)

    def _search_index(self, search_query, **data):

        sim_weight = data.get('sim_weight', 0.7)
        pr_weight  = data.get('pr_weight', 0.7)
        bert_weight = data.get('bert_weight', 0.7)

        terms = normalize_corpus([search_query], lemmatize=False, only_text_chars=True, tokenize=True)[0]

        doc_matches  = self.term_index.loc[terms].sum(axis=0)[self.term_index.loc[terms].sum(axis=0).gt(0)].sort_values(ascending=False)
        pr_matches   = self.pr_index.loc[doc_matches.index]['score'].sort_values(ascending=False)
        bert_terms   = self.bert.get_similar_df(search_query).sort_values(by='sim', ascending=False)
        bert_terms   = bert_terms[bert_terms.sim.ge(0.8)].set_index('terms')
        bert_matches = self.bert_term_index.loc[bert_terms.index.tolist()]
        bert_matches = bert_matches.sum(axis=0)[bert_matches.sum(axis=0).gt(0)].sort_values(ascending=False)


        results = pd.concat([doc_matches,pr_matches,bert_matches], axis=1).fillna(0)
        results.columns = ['sim','pr','bert']
        results=(results-results.min())/(results.max()-results.min())
        results.sim = results.sim * sim_weight
        results.pr = results.pr * pr_weight
        results.bert = results.bert * bert_weight
        pre_results = results.copy().fillna(0)

        results = results.sum(axis=1).sort_values(ascending=False)

        df = self.doc_index.loc[results.index][['title', 'url', 'description']]

        return (df, pre_results)
