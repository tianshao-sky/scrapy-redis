# -*- coding: utf-8 -*-
import time

import scrapy
from fake_useragent import UserAgent
from scrapy_redis.spiders import RedisSpider

from ..items import AmazonItem


class YmxSpider(RedisSpider):
    name = 'ymx'
    allowed_domains = ['www.amazon.cn']
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sd_allcat_books_I1?ie=UTF8&node=658390051']
    redis_key = 'redis_key:url'
    headers = {
        'User-Agent': str(UserAgent().random),
        'cookies':{
            'session-id':'459-4568418-5692641',
            'ubid-acbcn':'459-5049899-3055220',
            'x-wl-uid':'1AK7YMFc9IzusayDn2fT6Topjz3iAOpR3EeA2UQSqco8fo5PbK2aCpyBA/fdPMfKFqZRHc4IeyuU=',
            'session-token':'"OH1wPvfOj6Tylq2nnJcdn5wyxycR/lqyGsGU3+lUtU4mbC0ZD9s8/4Oihd1BlskUQG8zRbLVs9vfWXuiJmnRlDT4x35ircp2uLxOLNYQ4j5pzdFJIqqoZUnhHSJUq2yK80P3LqH8An7faXRCPW9BIqX1wu0WmHlSS9vYAPKA/2SGdV9b//EljYjIVCBjOuR/dKRiYEeGK3li0RJOVz7+vMWg7Rnzbx89QxlbCp0WyquZyVxG6f2mNw=="',
            'csm-hit':'tb:0J5M3DH92ZKHNKA0QBAF+b-0J5M3DH92ZKHNKA0QBAF|1544276572483&adb:adblk_no',
            'session-id-time':'2082787201l'}
    }

    def parse(self, response):
        url_list = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]/div/li/span/a/@href').extract()
        # class_list = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]/div/li/span/a/span/text()').extract()

        # 取前两个大类型
        # for url,class_name in zip(url_list[:2],class_list[:2]):
        for url in url_list[:2]:
            yield scrapy.Request(url=url,callback=self.next_parse,headers=self.headers)

    def next_parse(self,response):
        url_list = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li/span/a/@href').extract()
        # class_list = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li/span/a/span/text()').extract()

        # 取前两个小类型
        # for url,class_name in zip(url_list[:1],class_list[:1]):
        for url in url_list[:2]:
            yield scrapy.Request(url=url,callback=self.then_parse,headers=self.headers)

    def then_parse(self,response):
        nodes = response.xpath('//div[@id="mainResults"]/ul/li')

        for node in nodes:
            item = AmazonItem()
            # 书名
            item['name'] = node.xpath('.//h2/text()').extract_first()
            # 时间
            item['time_'] = node.xpath('./div/div/div/div[2]/div/div[1]/span[last()]/text()').extract_first()
            # 作者
            item['author'] = "".join(node.xpath('./div/div/div/div[2]/div[1]/div[2]/span/text()').extract())
            # 类型
            item['book_type'] = node.xpath('.//h3/text()').extract_first()
            # 价格
            item['price'] = node.xpath('./div/div/div/div[2]/div[2]/div/div[last()]/a/span[last()]/text()').extract_first()
            # 售卖类型
            item['sell_type'] = node.xpath('./div/div/div/div[2]/div[2]/div/div[last()]/i/text()').extract_first()
            yield item

        url = response.xpath('//div[@class="a-text-center"]/ul/li[last()]/a/@href | //div[@class="img_header hdr noborder"]/div/span[last()]/a/@href').extract_first()
        if url:
            url = 'https://www.amazon.cn' + url
            yield scrapy.Request(url=url, callback=self.next_page,headers=self.headers)

    def next_page(self,response):
        nodes = response.xpath('//span[@data-component-type="s-search-results"]/div[1]/div')
        nodes.pop(-1)

        for node in nodes:
            item = AmazonItem()
            path = './/div[@class="a-section a-spacing-medium"]/div[2]/div[2]/div/'
            # 书名
            item['name'] = node.xpath(path+'div[1]//h2/a/span/text()').extract_first()
            # 作者
            item['author'] = "".join(node.xpath(path+'div[1]//div[@class="a-row a-size-base a-color-secondary"]/span/text()').extract())
            # 类型
            item['book_type'] = node.xpath(path+'div[2]//a[@class="a-size-base a-link-normal a-text-bold"]/text()').extract_first().strip()
            # 价格
            item['price'] = node.xpath(path+'div[2]//span[@class="a-offscreen"]/text()').extract_first()
            # 售卖类型
            item['sell_type'] = node.xpath(path+'div[2]//span[@class="s-self-operated aok-align-bottom aok-inline-block a-text-normal"]/text()').extract_first()
            yield item

        url = response.xpath(
            '//div[@class="a-text-center"]/ul/li[last()]/a/@href | //div[@class="img_header hdr noborder"]/div/span[last()]/a/@href').extract_first()

        time.sleep(2)
        if url:
            url = 'https://www.amazon.cn' + url
            yield scrapy.Request(url=url, callback=self.next_page, headers=self.headers)
