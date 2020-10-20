from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow=r'^(/wiki/)((?!:).)*$'),
            callback='parse_items',
            cb_kwargs={'is_article': True}),
            Rule(LinkExtractor(allow='.*'), callback='parse-items',
            cb_kwargs={'is_article': False})]

    def parse_items(self, response, is_article):
        print(response.url)
        url = response.url
        title = response.css('h1::text').extract_first()
        if is_article:
            text = response.xpath('//div[@id="mw-content-text"]//text()').extract()
            lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
            lastUpdated = lastUpdated.replace('This page was last edited on ', '')
            print(f"URL is: {url}")
            print(f"TITLE is: {title}")
            print(f"TEXT IS: {text}")
            print(f"LAST UPDATED: {lastUpdated}")
        else:
            print('This is not an article {}'.format(title))