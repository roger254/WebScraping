from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random


# catch 404 and server error
def get_url(url):
    try:
        html_ = urlopen(url)
    except HTTPError:
        return None
    return html_


# ensure no duplicate links
pages = set()


def get_links(article_url):
    global pages
    html = get_url("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html, features='html.parser')
    try:
        print(bs_obj.h1.get_text())
        print(bs_obj.find(id='mw-content-text').findAll('p')[0])
        print(bs_obj.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! No worries though!')

    expression = re.compile("^(/wiki/)")
    for link in bs_obj.find_all('a', href=expression):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # new page encountered
                new_page = link.attrs['href']
                print('------------\n' + new_page)
                pages.add(new_page)
                get_links(new_page)


# start from the home page
get_links("")
