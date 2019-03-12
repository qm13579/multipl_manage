# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['http://www.people.com.cn/']
    start_urls = ['http://www.people.com.cn//']

    def parse(self, response):
        for tag_a in Selector(response=response).xpath('//a'):
            print(tag_a.xpath('.//text()').extract_first())
