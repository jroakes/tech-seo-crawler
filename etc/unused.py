
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
    clean_text  =re.sub("\[\[Category:.+?\]\]", "", clean_text)  # categories
    clean_text = re.sub("\[\[[^\[\]]+\|([^\[\]]+)\]\]", "\\1", clean_text)  # [[link|textlink]]
    clean_text = re.sub("\[\[(.+?)\]\]", "\\1", clean_text)  # [[links]]
    clean_text = re.sub("\n(==+)\s*([^=]+)\s*\\1","\n\\2", clean_text) # remove == from titles
    clean_text = re.sub("'''([^']+)'''","\\1", clean_text) # remove ''' bold
    clean_text = re.sub("''([^']+)''","\\1", clean_text) # remove '' italics
    clean_text = re.sub("(align|class|style)\s*=\s*(\".+?\"|[^\"].+? )", "", clean_text)  # common in wikitables (align|class|style) etc
    clean_text = re.sub("\n\\|-.{0,20}","", clean_text) # clean wikitables new lines
    clean_text = re.sub("(\n\\|}|\n\\{\\| *[^\n]*)","", clean_text) # clean open/end of wikitables
    clean_text = re.sub("\n![^\\|]+\\|","\n", clean_text) # clean table headers
    clean_text = re.sub("\s*\\| *\w+ *= *(\"?#?[A-Za-z0-9]+\"?|\n)","", clean_text) # clean technical definitions (in templates and tables)
    clean_text = re.sub("(?:\\| *)+","|", clean_text) # compact
    clean_text = re.sub("\\n\\| *","\\n", clean_text) # trim |
    clean_text = re.sub("(File|Image):[^\\.]+?\\.(jpg|png|pdf|svg)","", clean_text, re.I) # file names

    orig = clean_text
    same = False
    while not same:
        clean_text = re.sub("\{\{[^\{]*?\}\}", "", clean_text, re.M)  # templates
        same = clean_text == orig
        orig = clean_text
    clean_text = re.sub("\[https?:.*?\]", "", clean_text)  # external links

    return ' '.join(clean_text.split())





def build_sites(sites, num_pages=10):

    if not sites or not isinstance(sites, list):
        raise SitesMissing('`site` is a required variable and should be a list of dictionaries.')

    today = datetime.date.today()
    dt = today.strftime('%Y-%m-%d')

    sites = [{'topic':s['topic'], 'repo_name':s['repo_name'], 'repo_url': 'https://{}.github.io'.format(s['repo_name'])} for s in sites]

    data

    for site in sites:

        fdr = os.path.join('site', cfg.sg_save_folder ,'_'.join(site.split()))

        if not os.path.exists(fdr):
            os.makedirs(fdr)

        pages = get_wikipedia_pages(site,n=num_pages)

        for page in pages:

            topic   = page['title']
            title   = "{} | {}".format( topic, site )
            content = add_paragraphs(page['content'])

            fn = os.path.join(fdr , dt + '-' + '-'.join(topic.split()) + '.md')

            with open(fn, "w", encoding="utf-8") as html_file:
                html_file.write(PAGE_TEMPLATE.format(title=title.title(), topic=topic.title(), content=content ))
