from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
import re


# catch 404 and server error
def get_url(url):
    try:
        html_ = urlopen(url)
    except HTTPError:
        return None
    return html_


html = get_url("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html, features='html.parser')
expression = re.compile("../img/gifts/img.*.jpg")

images = bs_obj.find_all(
    'img',
    {
        'src': expression
    }
)
for image in images:
    print(image['src'])
