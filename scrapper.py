import json
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

random.seed(datetime.datetime.now())


# catch 404 and server error
def get_url(url):
    try:
        html_ = urlopen(url)
    except HTTPError:
        return None
    return html_


def get_links(article_url):
    html = get_url('http://en.wikipedia.org' + article_url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    expression = re.compile("^(/wiki/)((?!:).)*$")
    return bs_obj.find('div', {'id': 'bodyContent'}).findAll('a', href=expression)


def get_history_ips(page_url):
    # Format of revision history pages
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    page_url = page_url.replace('/wiki/', '')
    history_url = 'http://en.wikipedia.org/w/index.php?title=' + page_url + '&action=history'
    print('History url is' + history_url)
    html = get_url(history_url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    # finds only the links with class "mw-anonuserlink" which has IP addresses
    # instead of usernames
    ip_addresses = bs_obj.find_all('a', {'class': 'mw-anonuserlink'})
    address_list = set()
    for ip_address in ip_addresses:
        address_list.add(ip_address.get_text())

    return address_list


def get_country(ip_address):
    api_access = '0a41a2c00229ea80b86a87ef0ef1806e'

    response = get_url(
        'http://api.ipstack.com/' +
        ip_address +
        '?access_key=' + api_access
    )

    response_json = json.loads(response.read().decode('utf-8'))
    return response_json.get('country_code'), response_json.get('country_name')


links = get_links('/wiki/Python_(programming_language)')
while len(links) > 0:
    for link in links:
        print('-' * 20)
        history_ips = get_history_ips(link.attrs['href'])
        for history_ip in history_ips:
            country_code, country = get_country(history_ip)
            if country_code is not None and country is not None:
                print(history_ip + ' is from ' + country_code + '(' + country + ')')

    new_link = links[random.randint(0, len(links) - 1)].attrs['href']
    links = get_links(new_link)
