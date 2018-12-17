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


# return list of all linked articles
random.seed(datetime.datetime.now())


def get_links(article_url):
    html = get_url("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html, features='html.parser')

    # search and return only article links i.e '/wiki/sleepers'
    expression = re.compile("^(/wiki/)((?!:).)*$")
    body_div = bs_obj.find('div', {'id': 'bodyContent'}).findAll('a', href=expression)
    return body_div


links = get_links('/wiki/Kevin_Bacon')
while len(links) > 0:
    # extract the href attribute
    new_article = links[random.randint(0, len(links) - 1)].attrs['href']
    print(new_article)
    links = get_links(new_article)
