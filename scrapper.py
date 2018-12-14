from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup


# catch 404 and server error
def get_url(url):
    try:
        html_ = urlopen(url)
    except HTTPError:
        return None
    return html_


html = get_url("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html, features='html.parser')

found_objs = bs_obj.find(
    'table',
    {
        'id': 'giftList'
    }
)

for child in found_objs.descendants:
    print(child)
