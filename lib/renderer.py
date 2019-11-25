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

'''
Using: https://github.com/miyakogi/pyppeteer

Sample:
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://locomotive.agency/')
    await page.screenshot({'path': 'locomotive.png'})

    dimensions = await page.evaluate('() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
'''

import asyncio
import threading
import nest_asyncio
nest_asyncio.apply()
from pyppeteer import launch


class HTMLMissing(Exception):
    '''An exception for a missing or invalid HTML.'''
    pass



class RenderHTML():

    def __init__(self, html=None):

        self.html = ""

        asyncio.set_event_loop(asyncio.new_event_loop())

        self.set_html(html)
        asyncio.get_event_loop().run_until_complete(self.build_page())

    def set_html(self, html):
        self.html = html

    def html_set(self, html=None):
        if html or self.html:
            return html or self.html
        else:
            raise HTMLMissing('html is not set. Please run class.set_html(html) or pass the named `html` parameter to this function. ')

    async def build_page(self):
        browser = await launch(
                                handleSIGINT=False,
                                handleSIGTERM=False,
                                handleSIGHUP=False
                               )
        context = await browser.createIncognitoBrowserContext()
        self.page = await browser.newPage()

    def render(self,  html=None):
        html = self.html_set(html)
        return asyncio.get_event_loop().run_until_complete(self._render(html))

    async def _render(self, html):
        await self.page.setContent(html)
        dom = {}
        dom['title']        = await self.page.evaluate("() => [...document.querySelectorAll('title')].map( el => {return el.textContent;})")
        dom['description']  = await self.page.evaluate("() => [...document.querySelectorAll('meta[name=description]')].map( el => {return el.content;})")
        dom['h1']           = await self.page.evaluate("() => [...document.querySelectorAll('h1')].map( el => {return el.textContent;})")
        dom['h2']           = await self.page.evaluate("() => [...document.querySelectorAll('h2')].map( el => {return el.textContent;})")
        dom['links']        = await self.page.evaluate("() => [...document.querySelectorAll('a')].map( el => {return {'href': el.href, 'text': el.textContent, 'rel':el.rel};})")
        dom['images']       = await self.page.evaluate("() => [...document.querySelectorAll('img')].map( el => {return {'src': el.src, 'alt': el.alt};})")
        dom['canonical']    = await self.page.evaluate("() => [...document.querySelectorAll('link[rel=canonical]')].map( el => {return el.href;})")
        dom['robots']       = await self.page.evaluate("() => [...document.querySelectorAll('meta[name=robots]')].map( el => {return el.content;})")

        # Strip non-text
        await self.page.evaluate("document.querySelectorAll('script, iframe, style, noscript, link').forEach(function(el){el.remove()})", force_expr=True)
        content = await self.page.evaluate("document.body.textContent", force_expr=True)
        dom['content'] = ' '.join(content.split())
        return dom

    def extract_content(self, html=None):
        html = self.html_set(html)
        return asyncio.get_event_loop().run_until_complete(self._extract_content(html))

    def extract_links(self, html=None):
        html = self.html_set(html)
        return asyncio.get_event_loop().run_until_complete(self._extract_links(html))

    async def _extract_links(self, html):
        await self.page.setContent(html)
        links = await self.page.evaluate("() => [...document.querySelectorAll('a')].map( a => {return  {'href': a.href, 'text': a.textContent, 'rel':a.rel};})")
        return links

    async def _extract_content(self, html):
        await self.page.setContent(html)
        await self.page.evaluate("document.querySelectorAll('script, iframe, style, noscript, link').forEach(function(el){el.remove()})", force_expr=True)
        content = await self.page.evaluate("document.body.textContent", force_expr=True)
        return ' '.join(content.split())



def render_html(html):
    renderer = RenderHTML(html=html)
    return renderer.render()
