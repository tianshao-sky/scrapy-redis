# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ..items import AqistudyItem

class AqiSpider(RedisSpider):
    name = 'aqi'
    allowed_domains = ['www.aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'
    # start_urls = [base_url]
    redis_key = 'redis_keys:urls'

    def parse(self, response):
        url_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/@href").extract()
        city_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/text()").extract()

        # 取前5个城市
        for url, city in zip(url_list[:5], city_list[:5]):
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_month, meta={'city': city})

    def parse_month(self, response):
        url_list = response.xpath('//tbody/tr/td/a/@href').extract()

        # 取最新6月
        for url in url_list[-6:]:
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_day, meta={'city': response.meta['city']})

    def parse_day(self, response):
        item = AqistudyItem()
        node_list = response.xpath('//tr')

        # 去除标题行
        node_list.pop(0)

        for node in node_list:
            # 城市
            item['city'] = response.meta['city']
            # 日期
            item['data'] = node.xpath('./td[1]/text()').extract_first()
            # 空气质量指数
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            # 空气质量等级
            item['level'] = node.xpath('./td[3]/span/text()').extract_first()
            # pm2.5
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            # pm10
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            # so2
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            # co
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            # no2
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            # o3
            item['o3'] = node.xpath('./td[9]/text()').extract_first()

            yield item
