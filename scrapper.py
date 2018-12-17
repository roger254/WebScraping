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
random.seed(datetime.datetime.now())


# retrieve a list of all Internal links found on a page
def get_internal_links(bs_obj, include_url):
    internal_links = []
    # finds all links that begin with  '/'
    expression = re.compile("^(/|.*" + include_url + ")")
    for link in bs_obj.find_all('a', href=expression):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                internal_links.append(link.attrs['href'])

    return internal_links


# retrieves a list of all external links found in a page
def get_external_links(bs_obj, exclude_url):
    external_links = []
    # finds all links that start with 'http' or 'www' that do not
    # contain the current url
    expression = re.compile("^(http|www)((?!" + exclude_url + ").)*$")
    found = bs_obj.findAll('a', href=expression)
    for link in found:
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])

    return external_links


def split_address(address):
    address_parts = address.replace('https://', "").split("/")
    return address_parts


def get_random_external_link(starting_page):
    html = get_url(starting_page)
    bs_obj = BeautifulSoup(html, 'html.parser')
    external_links = get_external_links(bs_obj, split_address(starting_page)[0])
    if len(external_links) == 0:

        internal_links = get_internal_links(starting_page)

        return get_random_external_link(
            internal_links[random.randint(0, len(internal_links) - 1)]
        )
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_page):
    external_link = get_random_external_link(starting_page)
    print('Random external link is: ' + external_link)
    follow_external_only(external_link)


follow_external_only('https://oreilly.com')
