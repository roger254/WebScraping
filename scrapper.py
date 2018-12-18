import json
from urllib.error import HTTPError
from urllib.request import urlopen, urlretrieve
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


html = get_url('http://www.pythonscraping.com')
bsc_Obj = BeautifulSoup(html, 'html.parser')
image_location = bsc_Obj.find('a', {'id': 'logo'}).find('img')['src']
urlretrieve(image_location, 'logo.jpg')
