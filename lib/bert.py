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

import config as cfg

import torch
import pandas as pd
from tqdm import tqdm
from torch import nn
import transformers
from transformers import BertTokenizer, BertModel, DistilBertTokenizer, DistilBertModel

class BERT:

    def __init__(self, dims = None):

        if 'distilbert' in cfg.transformer_model:
            self.model      = DistilBertModel.from_pretrained(cfg.transformer_model)
            self.tokenizer  = DistilBertTokenizer.from_pretrained(cfg.transformer_model)
            self.model_dims = self.model.config.dim
        else:
            self.model      = BertModel.from_pretrained(cfg.transformer_model)
            self.tokenizer  = BertTokenizer.from_pretrained(cfg.transformer_model)
            self.model_dims = self.model.config.hidden_size

        # Make sure model is in Eval mode.
        self.model.eval()

        self.terms          = []
        self.embeddings     = torch.FloatTensor([])
        self.reduce         = nn.Linear(self.model_dims, dims) if dims else None
        self.activation     = nn.Tanh()
        self.sim_fn         = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)



    def add_terms(self, texts):

        for t in texts:
            self.add_term(t)


    def add_term(self, text):
        if text not in self.terms:
            emb   = self.get_embedding(text)
            self.terms.append(text)
            self.embeddings = torch.cat((self.embeddings, emb), dim=0)


    def get_embedding(self, text):

        with torch.no_grad():
            input_ids = torch.LongTensor(self.tokenizer.encode(text)).unsqueeze(0)
            lh  = self.model(input_ids)[0]
            emb = torch.mean(lh, dim=1)
            if self.reduce is not None:
                emb = self.reduce(emb)

        return self.activation(emb)


    def get_most_similar(self, term):
        emb = self.get_embedding(term)
        comp = emb.repeat(len(self.embeddings), 1)
        sim = self.sim_fn(self.embeddings, comp)
        best = sim.argmax().item()

        return self.terms[best], sim[best].item()


    def get_similar_df(self, term):
        emb = self.get_embedding(term)
        comp = emb.repeat(len(self.embeddings), 1)
        sim = self.sim_fn(self.embeddings, comp)
        df = pd.DataFrame(columns=['terms', 'sim'])
        df['terms'] = self.terms
        df['sim']   = sim.tolist()

        return df
