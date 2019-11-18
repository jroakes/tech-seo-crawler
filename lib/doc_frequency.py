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
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from lib.normalize import normalize_corpus



def get_tfidf(items, **data):

    ngram_range = data.get('ngram_range',(2, 5))
    min_df = data.get('min_df',3)
    top_n = data.get('top_n', 10)

    items = normalize_corpus(items)
    vectorizer = TfidfVectorizer(ngram_range=ngram_range, min_df = min_df)

    tvec_weights = vectorizer.fit_transform(items)

    weights = np.asarray(tvec_weights.mean(axis=0)).ravel().tolist()

    weights_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'weight': weights})

    top_features = weights_df.sort_values(by='weight', ascending=False).head(top_n)['term'].tolist()

    return top_features
