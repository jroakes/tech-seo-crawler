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


import pywikibot
import os
import re
import random
import datetime
from posixpath import join as urljoin
import time

import config as cfg

from web.publish import Publish
from lib.crawler import crawl_url



class SitesMissing(Exception):
    '''An exception for a missing or invalid sites variable.'''
    pass



def get_wikipedia_pages(query,n=5):

    sitew = pywikibot.Site("en", "wikipedia")

    results = []
    print('Looking up:', query)
    search = sitew.search(query, where='titles', get_redirects=False, total=int(n*5), content=True, namespaces="0")

    for page in search:
        if len(results) >= n:
            break
        title = page.title()
        title = re.sub(r"[^a-zA-Z\s0-9]+", "", title)
        url = page.full_url()
        print('\tGot:', title)
        text = crawl_url(url)['content']
        results.append({'title':title, 'content':text})

    return results


# https://github.com/valhallasw/plagiabot
def remove_wikitext(text):
    # clean some html/wikitext from the text before sending to server...
    # you may use mwparserfromhell to get cleaner text (but this requires dependency...)
    #remove refis
    if text is None or len(text) == 0: return ''
    refs = re.findall('<ref(?: .+?)?>(.*?)</ref>', text)
    for ref in refs:
        text = text.replace(ref, '')
    clean_text = pywikibot.textlib.removeHTMLParts(text, keeptags=['p'])
    clean_text = re.sub("\[https?:.*?\]", "", clean_text)  # external links
    clean_text  =re.sub(r" ?\[[^\]]+\] ?", "", clean_text)  # categories

    return ' '.join(clean_text.split())



def format_content(text):

    text = remove_wikitext(text)
    text_list = text.split('.')
    batch = []
    para_list = []
    for i, t in enumerate(text_list):
        batch.append( t.strip() +'.' )

        if len(batch) >= random.choice(range(4,7)) or i+1 == len(text_list):
            para_list.append(' '.join(batch))
            batch = []

    return "\n\n".join(para_list)


def build_site_data(sites, num_pages=10):

    if not sites or not isinstance(sites, list):
        raise SitesMissing('`site` is a required variable and should be a list of dictionaries.')

    today = datetime.date.today()
    page_date = today.strftime('%Y-%m-%d')

    sites = [{'topic':s['topic'], 'org_name':s['org_name']} for s in sites]

    data = {'folders':[], 'pages':{}}

    for site in sites:

        site_topic    = site['topic'].title()
        site_org_name = site['org_name'].lower()
        site_domain   = '{}.github.io'.format(site_org_name)
        site_host     = "https://" + site_domain

        local_folder = os.path.join('site', cfg.sg_save_folder ,'-'.join(site_org_name.split())).lower()

        data['folders'].append(local_folder)

        pages = get_wikipedia_pages(site_topic,n=num_pages)

        data['pages'][local_folder] = []

        for page in pages:

            page_topic      = page['title'].title()
            page_title      = "{} | {}".format( page_topic, site_topic ).title()
            page_content    = format_content(page['content'])

            page_slug       = '-'.join(page_topic.split()) + '.md'
            page_filename   = page_date + '-' + page_slug
            local_filename  = os.path.join( local_folder , page_filename )

            page_data = {
                            'page_topic'    : page_topic,
                            'page_title'    : page_title,
                            'page_content'  : page_content,
                            'local_folder'  : local_folder,
                            'local_filename': local_filename,
                            'site_host'     : site_host,
                            'site_domain'   : site_domain,
                            'site_topic'    : site_topic,
                            'page_slug'     : page_slug,
                            'page_filename' : page_filename,
                            'page_url'      : urljoin(site_host,page_slug)
                        }

            data['pages'][local_folder].append(page_data)

    return data


def add_links(sites, page):

    slug    = page['page_slug']
    content = page['page_content']

    other_pages = [p for fdr in sites for p in sites[fdr] if p['page_slug'] != slug]

    for op in other_pages:

        op_topic = op['page_topic']
        ts = op_topic.split()
        lw = [t for t in ts if len(t) == max([len(t) for t in ts])][0]

        op_topic += "|" + lw
        op_url = op['page_url'].replace('.md', '')

        content = re.sub(r"\s({})+\s".format(op_topic), r" [\1]({}) ".format(op_url), content, 1, flags=re.I)


    page['page_content'] = content

    return page


def build_sites(sg_sites = None, num_pages=10):

    sg_sites = sg_sites or cfg.sg_sites

    site_data = build_site_data(sg_sites, num_pages)

    folders = site_data['folders']

    for fdr in folders:
        if not os.path.exists(fdr):
            os.makedirs(fdr)

    sites = site_data['pages']

    for site in sites:

        pages = sites[site]

        for page in pages:

            page = add_links(sites, page)

            title           = page['page_title']
            topic           = page['page_topic']
            content         = bytes(page['page_content'], 'utf-8').decode('utf-8', 'ignore')

            local_filename  = page['local_filename']

            with open(local_filename, "w", encoding="utf-8") as html_file:
                html_file.write(cfg.sg_page_template.format(title=title.title(), topic=topic.title(), content=content ))


    return site_data



def publish_sites(site_data):

    folders = site_data['folders']

    for fdr in folders:

        org_name = os.path.basename(fdr)
        repo_name = '{}.github.io'.format(org_name)

        pb = Publish(cfg.sg_gh_user, org_name)

        status, response = pb.create_template_repo()
        if status in [200,201,202]:
            print('Created Repo:', status, response['name'])
        else:
            print('Could Not Create:', status, response['message'])
        time.sleep(2)

        pages = site_data['pages'][fdr]

        for page in pages:
            fp = page['local_filename']
            status, url = pb.publish_post(fp, path=None)
            print('\tUpdated File:', status, url)

        print()
