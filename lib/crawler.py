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

import config as cfg


class LinksExtractor(BaseExtractor):

    def extract(self):
        links = []
        items = self.parser.getElementsByTag(self.article.doc[0], 'a')
        for i in items:
            attr = {'href': self.parser.getAttribute(i, 'href'), 'text': self.parser.getText(i), 'rel': self.parser.getAttribute(i, 'rel')}
            if attr:
                links.append(attr)
        return links

class RobotsExtractor(BaseExtractor):

    def extract(self):
        robots = []
        kwargs = {'tag': 'meta', 'attr': 'name', 'value': 'robots'}
        items = self.parser.getElementsByTag(self.article.doc[0], **kwargs)
        for i in items:
            attr = self.parser.getAttribute(i, 'content')
            if attr:
                robots.append(attr)
        return robots



def crawl_url(url):
    g = Goose({'browser_user_agent': cfg.browser_user_agent, 'parser_class':'soup'})
    page = g.extract(url=url)
    infos = page.infos

    infos['final_url']       = page.final_url
    infos['link_hash']       = page.link_hash

    infos['links']          = LinksExtractor(g.config, page).extract()
    infos['meta']['robots'] = RobotsExtractor(g.config, page).extract()
    infos['content']        = ' '.join(page.cleaned_text.split())
    infos['html']           = ' '.join(page.raw_html.split())
    return infos
