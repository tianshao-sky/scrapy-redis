# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 书名
    name = scrapy.Field()
    # 时间
    time_ = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 类型
    book_type = scrapy.Field()
    # 价格
    price = scrapy.Field()
    #售卖类型
    sell_type = scrapy.Field()
    pass
