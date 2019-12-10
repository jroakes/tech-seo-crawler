# TechSEO Crawler


Build a small, 3 domain internet using Github pages and Wikipedia and construct a crawler to crawl, render, and index.

![TechSEO Screenshot](https://raw.githubusercontent.com/jroakes/tech-seo-crawler/master/etc/images/screenshot.png "TechSEO Screenshot")

Play with the results here: [Simple Crawler](http://ec2-34-233-22-11.compute-1.amazonaws.com:8501)

Slideshare is here: [Building a Simple Crawler on a Toy Internet](https://www.slideshare.net/jroakes/building-a-simple-crawler-on-a-toy-internet)

## Description

### Web Folder
In order to crawl a small internet of sites, we have to create it.  This tool creates 3 small sites from Wikipedia data and hosts them on Github Pages.  The sites are not linked to any other site on the internet, but are linked to each other.

### Main function

This tool attempts to implement a small ecosystem of 3 websites, along with a simple crawler, renderer, and indexer.  While the author did research to construct the repo, it was a design feature to prefer simplicity over complexity.  Items that are part of large crawling infrastructures, most notably disparate systems, and highly efficient code and data storage, are not part of this repo.  We focus on simple representations of items such that it is more accessible to newer developers.

#### Parts:
* PageRank
* Chrome Headless Rendering
* Text NLP Normalization
* Bert Embeddings
* Robots
* Duplicate Content Shingling
* URL Hashing
* Document Frequency Functions (BM25 and TFIDF)


Made for a presentation at [Tech SEO Boost](https://www.catalystdigital.com/techseoboost/)



## Getting Started

### Get the repo
```
git clone https://github.com/jroakes/tech-seo-crawler.git
```


### Dependencies

* Please see the requirements.txt file for a list of dependencies.

It is strongly suggested to do the following, first, in a new, clean environment.

* May need to install [Microsoft Build Tools] (http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe.) and upgrade setup tools  `pip install --upgrade setuptools` if you are on Windows.
* Install PyTorch `pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html`
* See requirements-libraries.txt file for remaining library requirements.  To install the frozen requirements this was developed with, use ```pip install -r requirements.txt```

Install with:
```
pip install -r requirements.txt
```


### Executing program

1. Make sure you've created your three sites first. See README file in the web folder. Conversely, if you just want to use the crawler/renderer, you can run with the premade sites and skip to step 3.
2. After creating your three sites, go to the config file and add the crawler_seed URL. This will be the organization name you created on github.io. For example: myorganization.github.io/
3. Run `streamlit run main.py` in the terminal or command prompt.  A new Browser window should open.
4. The tool can also be run interactively with the `Run.ipynb` notebook in Jupyter.


### Sharing
If you want to share your search engine for others to see, you can use Streamlit and Localtunnel.
1. Install Localtunnel `npm install -g localtunnel`
2. Start the tunnel with `lt --port 80 --subdomain <create a unique sub-domain name>`
3. Start the Streamlit server with `streamlit run main.py --server.port 80 --global.logLevel 'warning' --server.headless true --server.enableCORS false --browser.serverAddress <the unique subdomain from step 2>.localtunnel.me`
4. Navigate to `https://<the unique subdomain from step 2>.localtunnel.me` in your browser, or share the link with a friend.

#### Complete example:
In a new terminal:
```
npm install -g localtunnel
lt --port 80 --subdomain tech-seo-crawler
```

In another terminal:
```
cd /tech-seo-crawler/
activate techseo
streamlit run main.py --server.port 80 --global.logLevel 'warning' --server.headless true --server.enableCORS false --browser.serverAddress tech-seo-crawler.localtunnel.me
```


## Troubleshooting
* When running in streamlit we experienced a few connection closed errors during the Rendering process. If you experience this error just rerun the script by using the top right menu and clicking on rerun in streamlit.


## Contributors

Contributors names and contact info
* JR Oakes [@jroakes](https://twitter.com/jroakes)
* Robert Padgett [@robertcpadgett](https://twitter.com/robertcpadgett)


## Version History

* 0.1 - Alpha
    * Initial Release


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

### Libraries
* [ghPublish](https://github.com/oxalorg/ghPublish)
* [pandas](https://github.com/pandas-dev/pandas) # What would we all do without Pandas?
* [gensim](https://github.com/RaRe-Technologies/gensim)
* [pyppeteer](https://github.com/miyakogi/pyppeteer)
* [scikit-learn](https://github.com/scikit-learn/scikit-learn)
* [streamlit](https://github.com/streamlit/streamlit)
* [DIP](https://github.com/dipanjanS) # I don't know who you are, but thanks for my go-to text normalization pipeline.

### Topics
* https://github.com/kish1/PoliteCrawler/blob/master/polite_crawler.py
* https://bitbucket.org/mchaput/whoosh/src/default/
* https://www.ijarcce.com/upload/2016/january-16/IJARCCE%2052.pdf
* https://www.seltzer.com/margo/publications
* https://github.com/sidco0014/Search-Engine
* https://github.com/valerio94w/ADM-Hw3-Group4
* https://github.com/rw1993/hupubxj_search
* https://github.com/mitishagd/Information-Retrieval-System
* https://medium.com/startup-grind/what-every-software-engineer-should-know-about-search-27d1df99f80d
* http://web.stanford.edu/class/cs276/
* https://github.com/wuyi1405/brianspiering-nlp-course
* https://www.cs.toronto.edu/~muuo/blog/build-yourself-a-mini-search-engine/
