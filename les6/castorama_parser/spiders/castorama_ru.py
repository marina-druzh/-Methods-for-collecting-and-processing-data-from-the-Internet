import scrapy
from scrapy.http import HtmlResponse
from items import CastoramaParserItem
from scrapy.loader import ItemLoader


class CastoramaRuSpider(scrapy.Spider):
    name = 'castorama_ru'
    url = 'https://www.castorama.ru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'product-card__name')]")
        for link in links:
            yield response.follow(link, callback=self.goods_parse)

    def goods_parse(self, response: HtmlResponse):
        # Пришлось сделать так, иначе получить текс у меня не получалось
        price = response.xpath("//span[@class='price']//text()").extract()
        img = response.xpath("//div[@class='js-zoom-container']//@data-src").getall()
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        # loader.add_xpath('price', "//span[@class='price']/text()")
        loader.add_value('price', price)
        loader.add_value('link', response.url)
        # loader.add_value('images', "//div[@class='js-zoom-container']//@data-src")
        loader.add_value('images', img)
        yield loader.load_item()
