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

##################################################################################################################
# Crawler Settings
##################################################################################################################

# Enter the User-Agent to crawl as.
browser_user_agent = "Googlebot"

# How quickly we crawl a website.
per_sec_crawl_rate = 1



##################################################################################################################
# BERT settings
##################################################################################################################

# Models Available:
# * bert-base-uncased
# * bert-large-uncased
# * bert-base-cased
# * bert-large-cased
# * distilbert-base-uncased

# Enter the User-Agent to crawl as.
transformer_model = "bert-base-uncased"
embedding_size = 100



##################################################################################################################
# Site Generator Settings
##################################################################################################################

# the tool expects for a folder named `web` to exist.  This is the folder within where the website files are stored.
sg_save_folder = 'files'

# The username for your main Github Account.
sg_gh_user = 'jroakes-locomotive'

# Dictonary of your sites where `topic` is the name of the topic to search Wikipedia for, \
# and org_name is the EXACT name of the Github Organizations you created.
sg_sites = [
            {'topic': 'python software', 'org_name': 'python-software'},
            {'topic': 'data science', 'org_name': 'data-science-blog'},
            {'topic': 'search engine optimization', 'org_name': 'search-engine-optimization-blog'}
           ]







# This should not be changed unless you know what you are doing.
sg_page_template = '''---
layout: post
title:  {title}
categories: [{topic}]
---

{content}

'''
