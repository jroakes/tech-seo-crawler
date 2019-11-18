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

# Needed Libraries
def warn(*args, **kwargs):
    pass
import warnings
# Silly workaround to get rid of Sklearn deprication warnings.
warnings.warn = lambda *a, **b : None
import mmh3
from nltk import ngrams
import numpy as np
import pandas
import random
import argparse
from tqdm import tqdm

# Functions and Classes
def generate_random_seeds(n, seed=5):
    random.seed(seed)
    return random.sample(range(1, n+1), n)

def jaccard_similarity(set_a, set_b):
    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))


class ShingledText:
    def __init__(self, text, random_seed=5, shingle_length=5, minhash_size=200):
        split_text = text.split()
        if len(split_text) < shingle_length:
            raise ValueError(u'input text is too short for specified shingle length of {}'.format(shingle_length))

        self.minhash = []
        self.shingles = ngrams(split_text, shingle_length)

        for hash_seed in generate_random_seeds(minhash_size, random_seed):
            min_value = float('inf')
            for shingle in ngrams(split_text, shingle_length):
                value = mmh3.hash(' '.join(shingle), hash_seed)
                min_value = min(min_value, value)
            self.minhash.append(min_value)

    def similarity(self, other_shingled_text):
        return jaccard_similarity(set(self.minhash),
                set(other_shingled_text.minhash))


def apply_shingled(row,urls,shingles):

    url = row['address']
    urli = urls.index(url)
    urlsh = shingles[urli]
    high = 0.0
    match = ""
    start = 0

    if not urlsh:
        row['Sim Score'] = 0.0
        row['Sim Match'] = ""
        return row

    for i, sh in enumerate(shingles):

        if not urli == i and sh:
            sim = jaccard_similarity(set(urlsh), set(sh))
            if sim > high:
                high = sim
                match = urls[i]

    row['Sim Score'] = high
    row['Sim Match'] = match

    return row


def build_shingles(domain, url, content, ngram_length=5, minhash_size=100):

    if isinstance(content, str) and len(content.split()) > ngram_length:
        return ShingledText(content, shingle_length=ngram_length, minhash_size=minhash_size).minhash
    else:
        return np.zeros(minhash_size, dtype=np.int8).tolist()
