# -*- coding: utf-8 -*-
import scrapy
from ..items import EuropaItem


class TreasurySpider(scrapy.Spider):
    name = 'treasury'
    allowed_domains = ['http://www.treasury.gov.za']
    start_urls = ['http://www.treasury.gov.za/']

    def parse(self, response):
        pass


