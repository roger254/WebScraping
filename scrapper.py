import re
from urllib.request import urlopen, HTTPError

import pymysql
from bs4 import BeautifulSoup

conn = pymysql.connect(
    host='127.0.0.1',
    user='',
    password='',
    db='mysql'
)

cur = conn.cursor()
cur.execute('USE wikipedia')


def get_url(url):
    try:
        html = urlopen(url)
    except HTTPError:
        return None
    return html


def insert_page_if_not_exists(url):
    cur.execute('SELECT * FROM wikipedia.pages WHERE url = %s', url)
    if cur.rowcount == 0:
        cur.execute('INSERT INTO wikipedia.pages (url) VALUES (%s)', url)
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]


def insert_link(from_page_id, to_page_id):
    cur.execute(
        'SELECT * FROM wikipedia.links WHERE fromPageId = %s AND toPageId = %s',
        (int(from_page_id), int(to_page_id))
    )
    if cur.rowcount == 0:
        cur.execute(
            'INSERT INTO wikipedia.links (fromPageId, toPageId) VALUES (%s, %s)',
            (int(from_page_id), int(to_page_id))
        )
        conn.commit()


pages = set()


def get_links(page_url, recursion_level):
    global pages
    if recursion_level > 4:
        return
    page_id = insert_page_if_not_exists(page_url)
    html = get_url('http://en.wikipedia.org' + page_url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    expression = re.compile('^(/wiki/)((?!:).)*$')
    for link in bs_obj.find_all('a', href=expression):
        insert_link(
            page_id,
            insert_page_if_not_exists(link.attrs['href'])
        )
        if link.attrs['href'] not in pages:
            new_page = link.attrs['href']
            pages.add(new_page)
            get_links(new_page, recursion_level + 1)


get_links('/wiki/Kevin_Bacon', 0)

cur.close()
conn.close()
