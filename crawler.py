import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()

# Retrieve a list of all Internal links foound on a page.
def getInternalLinks(bs, includeUrl):
    includeUrl = f'{urlparse(includeUrl).scheme}://{urlparse(includeUrl).netloc}'
    internalLinks = []
    # Finds all links thhat begin with a "/"
    for link in bs.find_all('a',
        href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if link.attrs['href'].startswith('/'):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

# Retrieves a list of all external links found on a pagee.
def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    # Finds all links that starts with "http" that do
    # not contain the current URL
    for link in bs.find_all('a',
        href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):
    html = requests.get(startingPage)
    bs = BeautifulSoup(html.text, 'html.parser')
    externalLinks = getExternalLinks(bs, 
        urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one.')
        domain = f'{urlparse(startingPage).scheme}://{urlparse(startingPage).netloc}'
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = requests.get(siteUrl)
    domain = f"{urlparse(siteUrl).scheme}://{urlparse(siteUrl).netloc}"
    bs = BeautifulSoup(html.text, 'html.parser')
    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print(f"Random external link is: {externalLink}")
    followExternalOnly(externalLink)


