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


html = get_url("http://bit.ly/1Ge96Rw")
bs_obj = BeautifulSoup(html, features='html.parser')
# .findAll(tag, attributes, recursive=True, text='sample text', limit = > 1, keywords)
name_list = bs_obj.find_all(
    'span',
    {
        'class': 'green'
    }
)
for name in name_list:
    print(name.get_text())


