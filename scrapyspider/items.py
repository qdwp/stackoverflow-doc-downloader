# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StackItem(scrapy.Item):
    topic_id = scrapy.Field()
    topic_content = scrapy.Field()
    index_1 = scrapy.Field()
    index_2 = scrapy.Field()
    index_3 = scrapy.Field()
    title_id = scrapy.Field()
    title_content = scrapy.Field()
    context_id = scrapy.Field()
    context_head = scrapy.Field()
    context_content = scrapy.Field()
