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


from lib.robots import check_robots_txt
from lib.shingling import build_shingles
from lib.database import *
from lib.renderer import *
from lib.crawler import crawl_url

from web.site_generator import build_site_data, build_sites, publish_sites
from web.publish import Publish

import config as cfg

# Robots.txt
assert check_robots_txt('https://locomotive.agency/robots.txt', 'https://locomotive.agency/wp-admin/') == False
assert check_robots_txt('https://locomotive.agency/robots.txt', 'https://locomotive.agency/') == True


# Shingling
content_valid = "You know that you want your website to rank well, but where do you start? There is a gamut of optimization efforts that go much deeper than good content structure and using the right keywords. In fact, many of the most important ranking factors are much more technical and “behind the scenes”. At Locomotive, our technical team can uncover and resolve these elusive technical SEO issues, whereas other agencies can only begin to scratch the surface."
content_not_valid = "nothing"
assert build_minhash(content_valid, ngram_length=5, minhash_size=10).minhash == [-2087495345, -2133526056, -2107069758, -2122401432, -2111672224, -2007258663, -2128677349, -2141142084, -2055117892, -2142619357]
assert build_minhash(content_not_valid, ngram_length=5, minhash_size=10).minhash == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

content1 = """Many packages don't create a build for every single release which forces your pip to build from source. If you're happy to use the latest pre-compiled binary version, use --only-binary :all: to allow pip to use an older binary version."""
content2 = """Most packages don't create a build for every single release which forces your pip to build from source. If you're happy to use the latest pre-compiled binary version, use --only-binary :all: to allow pip to use an older binary version."""
content3 = """The C++ Build Tools allow you to build C++ libraries and applications targeting Windows desktop. They are the same tools that you find in Visual Studio 2019, Visual Studio 2017, and Visual Studio 2015 in a scriptable standalone installer. Now you only need to download the MSVC compiler toolset you need to build C++ projects on your build servers."""

hashdb = HashLookup()

hashdb.add_hash('content1', content1)
hashdb.add_hash('content2', content2)
hashdb.add_hash('content3', content3)

assert len(hashdb) == 3
assert hashdb.get_hash('content1')[:5] == [-2145608475, -2092676559, -2100324990, -2106062289, -2101729913]
assert hashdb.get_similar(content2, threshold=0.9) == ['content2']



# rendering
with open("files/demo.html", "r") as f:
    html = f.read()
renderer = RenderHTML(html=html)
assert renderer.render() == {'title': ['Example Domain'], 'description': [], 'h1': ['Example Domain'], 'h2': [], 'links': [{'href': 'https://www.iana.org/domains/example', 'text': 'More information...', 'rel': ''}], 'images': [], 'canonical': [], 'robots': [], 'content': 'Example Domain This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission. More information...'}
assert renderer.extract_content() == 'Example Domain This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission. More information...'
assert renderer.extract_links() == ['https://www.iana.org/domains/example']


# Crawling
info = crawl_url('http://example.com/')
assert info['meta']['robots'] == []
assert info['meta']['canonical'] == 'http://example.com/'
assert info['domain'] == 'example.com'
assert info['title'] == 'Example Domain'



print('All Tests Passed')
