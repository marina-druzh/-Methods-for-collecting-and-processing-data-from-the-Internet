import scrapy


class GbRuSpider(scrapy.Spider):
    name = 'gb_ru'
    allowed_domains = ['gb.ru']
    start_urls = ['http://gb.ru/']

    def parse(self, response):
        pass
