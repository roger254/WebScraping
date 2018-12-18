import pymysql
import datetime
import random
import re
from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup

conn = pymysql.connect(
    host='127.0.0.1',
    user='',
    password='',
    db='mysql'
)

cur = conn.cursor()
cur.execute('USE scraping')

random.seed(datetime.datetime.now())


def store(title, content):
    cur.execute(
        'INSERT INTO pages (title, content) VALUES (%s,%s)',
        (title, content)
    )
    cur.connection.commit()


def get_url(url):
    print(url)
    try:
        html = urlopen(url)
    except HTTPError:
        return None
    return html


def get_links(article_url):
    html = get_url('http://en.wikipedia.org' + article_url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    title = bs_obj.find('h1').get_text()
    content = bs_obj.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    if len(content) > 1:
        store(title, content)
    expression = re.compile('^(/wiki/)((?!:).)*$')
    return bs_obj.find('div', {'id': 'bodyContent'}).findAll('a', href=expression)


links = get_links('/wiki/Kevin_Bacon')
try:
    while len(links) > 0:
        new_article = links[random.randint(0, len(links) - 1)].attrs['href']
        print(new_article)
        links = get_links(new_article)
finally:
    cur.close()
    conn.close()
