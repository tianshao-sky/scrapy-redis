# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient

class AqistudyPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient(host="127.0.0.1", port=27017, )

    def process_item(self, item, spider):
        aqi_dict = dict(item)
        # 城市
        city = aqi_dict.pop('city')

        # database：aqi，collection：各个城市名
        db = self.client.aqi[city]
        db.insert(aqi_dict)
        return item

