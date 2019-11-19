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


import networkx as nx
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
from urllib.parse import urlparse


def build_pagerank_df(url_list, link_tuples):

    pr_graph = run_graphs(url_list, link_tuples)

    # Calculate scores
    scores_pr = nx.pagerank(pr_graph, max_iter=1000)

    # Sort scores
    ranked_nodes_pr = sorted(((scores_pr[s],s) for i,s in enumerate(list(scores_pr.keys()))), reverse=True)

    data = [{'url':u, 'score':s} for s, u in ranked_nodes_pr]

    return pd.DataFrame(data)



def run_graphs(addresses, links):

    '''
    addresses: List of strings.
    links: List of tuples as (source, destimation) pairs.
    '''

    G = nx.DiGraph()

    G.add_nodes_from(addresses)
    G.add_edges_from(links)


    return G
