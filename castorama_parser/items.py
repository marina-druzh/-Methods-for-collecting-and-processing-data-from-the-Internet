# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst

def process_price(value):
    money = 0
    if value:
        money = int(value[2].replace(' ',''))
    return money


class CastoramaParserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(  
        input_processor=Compose(process_price),
        output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    _id = scrapy.Field()
