# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
url_dict={
    'people':'http://www.people.com.cn//',
          }

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['http://www.people.com.cn/']
    start_urls = ['http://www.people.com.cn//']

    def parse(self, response):
        fun_key=match_url(response.url)
        obj=getattr(NewsSpider,fun_key)
        obj(self,response)

    def people(self,response):
        '''处理people相关信息'''
        for tag_a in Selector(response=response).xpath('//a'):
            tag_a.xpath('.//text()').extract_first()
        print('处理完成')
def match_url(url):
    for k,v in url_dict.items():
        response=re.findall('.*%s.*'%v,url)
        if response:
            return k
        else:
            return False