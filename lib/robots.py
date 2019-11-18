#! /usr/bin/env python
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


# https://developers.google.com/search/reference/robots_txt
# Python Implementation by Moz
## https://github.com/seomoz/reppy

'''
Using: https://github.com/seomoz/reppy
Sample:
from reppy.robots import Robots

# This utility uses `requests` to fetch the content
robots = Robots.fetch('https://locomotive.agency/robots.txt')
print(robots.allowed('https://locomotive.agency/wp-admin/', 'googlebot'))

# Get the rules for a specific agent
agent = robots.agent('googlebot')
print(agent.allowed('https://locomotive.agency/wp-admin/'))
'''

from reppy.robots import Robots


def check_robots_txt(sitemap, url, user_agent="googlebot"):
    '''
    Arguments:
    sitemap: String
    url: String
    user_agent String default: googlebot
    '''
    robots = Robots.fetch(sitemap)
    agent = robots.agent(user_agent)
    return agent.allowed(url)
