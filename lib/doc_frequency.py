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
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from lib.normalize import normalize_corpus

import gensim
from gensim.summarization.bm25 import get_bm25_weights

import config as cfg



def get_tfidf(docs, doc_index):

    docs_norm = normalize_corpus(docs, lemmatize=False,
                     only_text_chars=True,
                     tokenize=False, sort_text=False)

    vectorizer = TfidfVectorizer()
    weights = vectorizer.fit_transform(docs_norm).transpose().toarray()
    terms = vectorizer.get_feature_names()

    inv_idx = pd.DataFrame(weights, index=terms, columns=doc_index)


    #     	          0 	 1 	     2 	        3 	     4        	5          6         7 	     8 	     9
    # context 	     0.0 	0.0 	0.0 	1.507414 	0.0 	1.507414 	0.706484 	0.0 	0.0 	0.0
    # prevent 	     0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.914903 	0.0 	0.0 	0.0
    # altogether 	 0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.000000 	0.0 	0.0 	0.0

    return inv_idx



def get_tfidf_bert(docs, doc_index):

    docs_norm = normalize_corpus(docs, lemmatize=False,
                     only_text_chars=True,
                     tokenize=False, sort_text=False)

    vectorizer = TfidfVectorizer(ngram_range=[4,4], max_df=1.0)

    weights = vectorizer.fit_transform(docs_norm).transpose().toarray()
    terms = vectorizer.get_feature_names()

    inv_idx = pd.DataFrame(weights, index=terms, columns=doc_index)


    #     	          0 	 1 	     2 	        3 	     4        	5          6         7 	     8 	     9
    # context 	     0.0 	0.0 	0.0 	1.507414 	0.0 	1.507414 	0.706484 	0.0 	0.0 	0.0
    # prevent 	     0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.914903 	0.0 	0.0 	0.0
    # altogether 	 0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.000000 	0.0 	0.0 	0.0

    return inv_idx


def get_bm25(docs, doc_index):

    docs_norm = normalize_corpus(docs, lemmatize=False,
                     only_text_chars=True,
                     tokenize=True, sort_text=False)

    bm = gensim.summarization.bm25.BM25(docs_norm)

    terms = {t:bm.get_scores([t]) for t in set(t for df in bm.doc_freqs for t in df.keys())}

    # Build Dataframe and transpose it.
    inv_idx = pd.DataFrame(terms).T

    inv_idx.columns = doc_index

    #     	          0 	 1 	     2 	        3 	     4        	5          6         7 	     8 	     9
    # context 	     0.0 	0.0 	0.0 	1.507414 	0.0 	1.507414 	0.706484 	0.0 	0.0 	0.0
    # prevent 	     0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.914903 	0.0 	0.0 	0.0
    # altogether 	 0.0 	0.0 	0.0 	0.000000 	0.0 	0.000000 	0.000000 	0.0 	0.0 	0.0

    return inv_idx
