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

from engine import *

import streamlit as st
import copy
from lib.utils import ClassStorage

import config as cfg

storage = ClassStorage()

def crawl_data(seed):
    fn = 'crawler.pkl'
    loaded = storage.load_pickle(fn)
    if loaded:
        st.markdown('Loaded saved file.')
        return loaded
    crawler = Crawler()
    crawler.crawl(seed)
    storage.save_pickle(fn, crawler)
    return crawler

def render_data(crawler):
    fn = 'render.pkl'
    loaded = storage.load_pickle(fn)
    if loaded:
        st.markdown('Loaded saved file.')
        return loaded
    crawler.render()
    storage.save_pickle(fn, crawler)
    return crawler

def bert_data(indexer):
    fn = 'bert.pkl'
    loaded = storage.load_pickle(fn)
    if loaded:
        st.markdown('Loaded saved file.')
        return loaded
    indexer.build_bert_embeddings_st()
    storage.save_pickle(fn, indexer.bert)
    return indexer.bert

def index_data(crawler, i_type, title_boost):
    fn = 'indexer{i_type}_{title_boost}.pkl'.format(i_type=i_type, title_boost=title_boost)
    loaded = storage.load_pickle(fn)
    if loaded:
        st.markdown('Loaded saved file.')
        loaded.bert = bert_data(indexer)
        return loaded
    indexer = Indexer(crawler)
    indexer.build_index(i_type=i_type, title_boost=title_boost)
    storage.save_pickle(fn, indexer)
    indexer.bert = bert_data(indexer)
    return indexer


def main():

    st.title('Crawling and Rendering in Python')

    st.sidebar.markdown('## Indexing Options')
    i_type       = st.sidebar.radio('Term Frequency type?',('bm25', 'tfidf'))
    title_boost  = st.sidebar.slider('How much of a boost to give titles?', 1, 5, 2, 1)

    st.sidebar.markdown('## Search Options')
    search_query    = st.sidebar.text_input('Search Query', '')
    sim_weight      = st.sidebar.slider('How much weight to give to term similarity?', 0.0, 1.0, 0.5, 0.1)
    pr_weight       =  st.sidebar.slider('How much weight to give to PageRank?', 0.0, 1.0, 0.5, 0.1)
    bert_weight     = st.sidebar.slider('How much weight to give to bert?', 0.0, 1.0, 0.5, 0.1)


    st.markdown('## Crawling')
    # Crawling (First Wave)
    crawler = crawl_data(cfg.crawler_seed)
    st.markdown('Crawling Complete')

    st.markdown('## Rendering')
    # Rendering (Second Wave)
    crawler = render_data(crawler)
    st.markdown('Rendering Complete')

    st.markdown('## Indexing')
    # Build the index
    indexer = index_data(crawler, i_type, title_boost)
    st.markdown('Indexing Complete')

    st.markdown('## Searching: {}'.format(search_query))

    if len(search_query):
        data = {'sim_weight':sim_weight, 'pr_weight':pr_weight, 'bert_weight':bert_weight}
        df, pre_results = indexer.search_index_st(search_query, **data)
        st.markdown('### Ranking Data')
        st.dataframe(pre_results, width=1000)
        st.markdown('### Search Results')
        for i, row in df.iterrows():
            desc = row['description'] if len(row['description']) < 280 else  row['description'][:280] + '...'
            st.markdown('#### [{}]({}) \n {} \n {}'.format(row['title'], row['url'], row['url'], desc))

    else:
        st.markdown('You need to enter a search term.')


main()
