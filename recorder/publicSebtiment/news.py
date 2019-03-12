# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['http://www.people.com.cn/']
    start_urls = ['http://http://www.people.com.cn//']

    def parse(self, response):
        pass
