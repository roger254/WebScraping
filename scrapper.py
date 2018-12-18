import os
from urllib.error import HTTPError
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

download_dir = 'download'
base_url = 'http://pythonscraping.com'


# catch 404 and server error
def get_url(url):
    try:
        html_ = urlopen(url)
    except HTTPError:
        return None
    return html_


def get_absolute_url(base_url_, source):
    if source.startswith('http://www.'):
        url = 'http://' + source[11:]
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://' + source
    else:
        url = base_url_ + '/' + source
    if base_url_ not in url:
        return None
    return url


def get_download_path(base_url_, absolute_url, download_dir_):
    path = absolute_url.replace('www.', '')
    path = path.replace(base_url_, '')
    path = download_dir_ + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path


html = get_url('http://www.pythonscraping.com')
bsc_Obj = BeautifulSoup(html, 'html.parser')
download_list = bsc_Obj.findAll(src=True)

for download in download_list:
    file_url = get_absolute_url(base_url, download['src'])
    if file_url is not None:
        print(file_url)
        urlretrieve(
            file_url,
            get_download_path(base_url, file_url, download_dir)
        )
