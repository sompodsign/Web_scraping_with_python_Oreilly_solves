#! python3
#! data_printing_from_wiki.py - collects all titles and print.

import requests, re
from bs4 import BeautifulSoup

pages = set()

def getLinks(articleUrl):
    html = requests.get(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html.text, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('spam').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing...')
    
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print('-' * 20)
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)

getLinks('')

