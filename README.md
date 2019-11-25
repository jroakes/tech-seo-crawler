# TechSEO Crawler


Build a small, 3 domain internet using Github pages and Wikipedia and construct a crawler to crawl, render, and index.


## Description

### Web Folder
In order to crawl a small internet of sites, we have to create it.  This tool creates 3 small sites from Wikipedia data and hosts them on Github Pages.  The sites are not linked to any other site on the internet, but are linked to each other.

### Main function

This tool attempts to implement a small ecosystem of 3 websites, along with a simple crawler, renderer, and indexer.  While the author did research to construct the repo, it was a design feature to prefer simplicity over complexity.  Items that are part of large crawling infrastructures, most notably disparate systems, and highly efficient code and data storage, are not part of this repo.  We focus on simple representations of items such that it is more accessible to newer developers.

#### Parts:
* PageRank
* Chrome Hadless Rendering
* Text NLP Normalization
* Bert Embeddings
* Robots
* Duplicate Content Shingling
* URL Hashing
* Document Frequency Functions (BM25 and TFIDF)


## Getting Started

### Dependencies

* Please see the requirments.txt file for a list of dependencies.

It is strongly suggested to do the following, first, in a new, clean environment.

* May need to install [Microsoft Build Tools] (http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe.) and upgrade setup tools  `pip install --upgrade setuptools` if you are on Windows.
* Install PyTorch `pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html`
* See requirements.txt file for remaining requirements.  Normally installed with ```pip install -r requirements.txt```

Install with:
```
pip install -r requirements.txt
```


### Executing program

* Run `streamlit run main.py` in the terminal or command prompt.  A new Browser window should open.
* The tool can also be run interactively with the `Run.ipynb` notebook in Jupyter.


## Authors

Contributors names and contact info

JR Oakes
[@jroakes](https://twitter.com/jroakes)


## Version History

* 0.1 - Alpha
    * Initial Release


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [ghPublish](https://github.com/oxalorg/ghPublish)
* [gensim](https://github.com/RaRe-Technologies/gensim)
* [pyppeteer](https://github.com/miyakogi/pyppeteer)
* [scikit-learn](https://github.com/scikit-learn/scikit-learn)
* [DIP](https://github.com/dipanjanS)
