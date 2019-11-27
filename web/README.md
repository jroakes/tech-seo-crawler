# Building a Simple Internet of 3 Websites.

This section of the repo allows you to build a small, 3 domain internet using Github pages and Wikipedia.

## Description

In order to crawl a small internet of sites, we have to create it.  This tool creates 3 small sites from Wikipedia data and hosts them on Github Pages.  The sites are not linked to any other site on the internet, but are linked to each other.


## Getting Started

### Dependencies

* Please see the requirments.txt file for a list of dependencies.

Install with:
```
pip install -r requirements.txt
```


### Executing program

1. In Github, create three organizations under your user account.
* To do this go to the plus sign next to your profile photo at the top right. 
* Select the plan you want to use. Using the free Open Source plan should work fine.
* Name your organization, add email and select My personal account.
2. Update `sg_gh_user` in `config.py` with your Github username.
3. Once created, edit the `config.py` file below, with a topic (broader topics will work better) and the *exact* organization name (org_name) from Github, for each separate site.
4. Run `python site_generator.py` and follow the prompts.  Note: This has not been fully tested with Github 2-factor authentication.

```
sg_sites = [
            {'topic': 'python software', 'org_name': 'python-software'},
            {'topic': 'data science', 'org_name': 'data-science-blog'},
            {'topic': 'search engine optimization', 'org_name': 'search-engine-optimization-blog'}
           ]
```

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
