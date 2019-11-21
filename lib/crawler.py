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


from goose3 import Goose
from goose3.extractors import BaseExtractor
from lib.utils import *

import config as cfg



class LinksExtractor(BaseExtractor):

    def extract(self, url):
        links = []
        items = self.parser.getElementsByTag(self.article._raw_doc, 'a')

        for i in items:
            href = get_canonical_url(self.parser.getAttribute(i, 'href'), url)
            attr = {'href': href, 'text': self.parser.getText(i) or '', 'rel': self.parser.getAttribute(i, 'rel') or ''}
            if attr:
                links.append(attr)
        return links


class RobotsExtractor(BaseExtractor):

    def extract(self):
        robots = []
        kwargs = {'tag': 'meta', 'attr': 'name', 'value': 'robots'}
        items = self.parser.getElementsByTag(self.article._raw_doc, **kwargs)
        for i in items:
            attr = self.parser.getAttribute(i, 'content')
            if attr and len(attr):
                attr = [a.strip().lower() for a in attr.split(',')]
                robots.extend(attr)
        return robots



def crawl_url(url):
    g = Goose({'browser_user_agent': cfg.browser_user_agent, 'parser_class':'soup'})
    r = g.fetcher.fetch_obj(url)
    html = r.content.decode('utf-8').strip()
    page = g.extract(raw_html=html)
    infos = page.infos

    infos['final_url']       = page.final_url
    infos['status']          = r.status_code
    infos['headers']         = r.headers
    infos['link_hash']       = page.link_hash
    infos['final_url']       = r.url
    infos['domain']          = get_hostname(r.url)
    infos['links']           = LinksExtractor(g.config, page).extract(url)
    infos['meta']['robots']  = RobotsExtractor(g.config, page).extract()
    infos['content']         = ' '.join(page.cleaned_text.split())
    infos['html']            = ' '.join(page.raw_html.split())
    return infos
