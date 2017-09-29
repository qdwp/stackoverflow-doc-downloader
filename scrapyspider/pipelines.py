# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

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

        #     _col_list.insert_one({"topic_id": item['topic_id'], "topic_content": item['topic_content']})
        # if _col_content.find({context_id: item['context_id']}).count() <= 0:
        #     _col_content.insert_one(item)
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
