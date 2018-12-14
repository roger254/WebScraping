from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup


# catch 404 and server error
def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None

    try:
        bs_obj = BeautifulSoup(html.read())
        title_ = bs_obj.body.h1
    except AttributeError:
        return None
    return title_


title = get_title('http://www.pythonscraping.com/exercises/exercise1.html')
if title is None:
    print('Title could not be found')
else:
    print(title)
