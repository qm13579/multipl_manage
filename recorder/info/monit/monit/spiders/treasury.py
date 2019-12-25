# -*- coding: utf-8 -*-
import scrapy
from ..items import EuropaItem
from info.removal import SpiderRemoval
from info.analysisSpider import analysisSpider
from ..items import EuropaItem

class TreasurySpider(scrapy.Spider):
    name = 'treasury'
    allowed_domains = ['http://www.treasury.gov.za']
    start_urls = ['http://www.treasury.gov.za/']
    #实例化模块
    sr = SpiderRemoval()
    analysis = analysisSpider()

    url_set = sr.urlSet(start_urls)
    def parse(self, response):
        item_list = self.analysis.herfCommonAnalysis(startUrl=self.start_urls,response=response,urlsSet=self.url_set)
        for item_dict in item_list:
            item_obj = EuropaItem(
                title=item_dict['title'],
                url=item_dict['href'],
                md5=item_dict['md5'],
                base_url=item_dict['base_url_id'],
                keyword_1=item_dict['keyword'][0],
                keyword_2=item_dict['keyword'][1],
                keyword_3=item_dict['keyword'][2],
                keyword_4=item_dict['keyword'][3],
                keyword_5=item_dict['keyword'][4],
            )
            if item_obj['title'] == 'ENGLISH': continue
            yield item_obj;


