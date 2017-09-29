## stackoverflow 文档下载器

### Scrapy 爬虫抓取数据保存到mongodb

### scrawl
```
#/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import hashlib
from time import sleep
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapyspider.items import StackItem

from ..util.convert import html2md, MD5

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Stackoverflow(Spider):
    name = "stack"
    allowed_domains = ['https://stackoverflow.com']
    start_urls = ['https://stackoverflow.com/documentation/go/topics']

    def parse(self, response):
        """抓取二级 URL"""
        all_pages = response.xpath('//span[@class="page-numbers"]/text()').extract()
        all_pages.sort(key=int, reverse=True)
        _all_pages = [int(item) for item in all_pages]

        page_list = ["{0}?page={1}&tab=popular".format(self.start_urls[0], index) for index in xrange(1, max(_all_pages) + 1)]

        for index, page in enumerate(page_list):
            sleep(3)
            yield Request(page, meta={"_index_1": index}, callback=self.parse_page, dont_filter=True)
            # break

    def parse_page(self, response):
        """解析列表URL"""
        _topics = response.xpath('//a[@class="doc-topic-link"]')

        for index, _top in enumerate(_topics):
            _url = _top.xpath('@href').extract_first()
            _title = _top.xpath('text()').extract_first()
            _item_url = self.allowed_domains[0] + _url
            print("====", _title)
            sleep(5)
            yield Request(_item_url,
                meta={"_index_1": response.meta['_index_1'], "_index_2": index},
                callback=self.parse_item, dont_filter=True)
            # break

    def parse_item(self, response):
        """解析元素"""

        content_head_list = response.xpath('//a[@class="doc-example-link"]/text()').extract()
        content_content_list = response.xpath('//div[@class="example-body-html prettyprint-override"]').extract()

        topic_group = re.match('.*/documentation/(.*?)/', response.url)
        _topic = topic_group.group(1)
        _topic_id = MD5(_topic)
        _index_1 = response.meta['_index_1']
        _index_2 = response.meta['_index_2']
        _title = response.xpath('//a[@class="doc-topic-link"]/text()').extract_first()

        _title_id = "{}_{}_{}".format(_index_1, _index_2, MD5(_title))

        _index = 0
        for head, content in zip(content_head_list, content_content_list):
            _context_head = head
            _context_head_id = "{}_{}_{}".format(_title_id, _index, MD5(_context_head))
            _context_content = html2md(content)

            item = StackItem()
            item['topic_id'] = _topic_id
            item['topic_content'] = _topic
            item['index_1'] = _index_1
            item['index_2'] = _index_2
            item['index_3'] = _index
            item['title_id'] = _title_id
            item['title_content'] = _title
            item['context_id'] = _context_head_id
            item['context_head'] = _context_head
            item['context_content'] = "### " + _context_head + "\n\n" +  _context_content

            print("==============")
            print(_topic, _title)

            yield item
            _index += 1
```

### pipline

```
import pymongo
from time import sleep
from pymongo import MongoClient


class ScrapyspiderPipeline(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['blog']

    def process_item(self, item, spider):
        print(("item == {} == {}".format(item['context_id'], item['context_head'])))

        topic = item['topic_content']
        _col_list = self.db["{}_list".format(topic)]
        _col_content = self.db["{}_content".format(topic)]

        if _col_list.find({"title_id": {"$in": [item['title_id']], "$exists": True }}).count() > 0:
            print("collection list duplicated")
        else:
            _col_list.insert_one({
                "topic_id": item['topic_id'],
                "topic_content": item['topic_content'],
                "title_id": item['title_id'],
                "title_content": item['title_content']
            })
        _col_content.insert_one({
            "topic_id": item['topic_id'],
            "topic_content": item['topic_content'],
            "index_1": item['index_1'],
            "index_2": item['index_2'],
            "index_3": item['index_3'],
            "title_id": item['title_id'],
            "title_content": item['title_content'],
            "context_id": item['context_id'],
            "context_head": item['context_head'],
            "context_content": item['context_content']
        })
        sleep(1)
        return item
```
