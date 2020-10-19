#! python3
#! crawl wikipedia

import requests, re
from bs4 import BeautifulSoup
import datetime
import random

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = requests.get(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs.find('div', {'id':'bodyContent'}).find_all(
        'a', href=re.compile('^(/wiki/)((?!:).)*$'))
    
links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)





# http://en.wikipedia.org/wiki/kevin_bacon