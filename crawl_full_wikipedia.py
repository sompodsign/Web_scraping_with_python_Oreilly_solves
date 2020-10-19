#! python3
#! crawl wikipedia

import requests, re
from bs4 import BeautifulSoup

pages = set()

def getLinks(articleUrl):
    html = requests.get(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html.text, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)

getLinks('')

