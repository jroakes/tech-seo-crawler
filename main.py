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

import config as cfg

@st.cache(persist=True, suppress_st_warning=True)
def crawl_data(seed):
    crawler = Crawler()
    crawler.crawl(seed)
    return crawler

@st.cache(persist=True, suppress_st_warning=True)
def render_data(crawler):
    newcrawler = copy.deepcopy(crawler)
    newcrawler.render()
    return newcrawler

@st.cache(persist=True, suppress_st_warning=True)
def index_data(crawler, i_type, title_boost):
    indexer = Indexer(crawler)
    indexer.build_index(i_type=i_type, title_boost=title_boost)
    indexer.build_bert_embeddings_st()
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
        df, doc_matches, pr_matches, bert_matches = indexer.search_index(search_query, **data)
        st.markdown('### Document Similarity Matches')
        st.dataframe(doc_matches)
        st.markdown('### By PageRank')
        st.dataframe(pr_matches)
        st.markdown('### Bert Matches')
        st.dataframe(bert_matches)
        st.markdown('### Search Results')
        st.dataframe(df)
    else:
        st.markdown('You need to enter a search term.')


main()
