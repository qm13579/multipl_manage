# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
import re
import sys,io
from ..items import EuropaItem
import sys, io
from urllib import parse
from info.models import WebInfo
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

class EurSpider(scrapy.Spider):
    name = 'eur'
    allowed_domains = ['ecb.europa.eu']
    # start_urls = ['https://www.ecb.europa.eu/','http://www.treasury.gov.za']
    start_urls = ['https://www.ecb.europa.eu/','http://www.treasury.gov.za']
    url_set=set()
    for i in WebInfo.objects.all():
        url_set.add(i)
    item_list = []
    def parse(self, response):
        # print(response.url)
        item_list = self.pdf_info(response=response)
        # print('---->')
        for item_dict in item_list:
            # 数据持久化
            if  item_dict['title'] =='ENGLISH' : continue
            # print(item_dict)
            item_obj = EuropaItem()
            item_obj['title']=item_dict['title']
            item_obj['url']=item_dict['href']
            item_obj['md5']=item_dict['md5']
            if  item_obj['title'] =='ENGLISH' : continue
            yield item_obj

            # 持久化url
            # content = Selector(response=response).xpath('//a/@href').extract()
            # for url in content:
            #     if len(url) < 2 :continue
            #     elif  not url.startswith('/') : continue
            #     elif url[1] == '/':continue
            #     url=self.start_urls[0]+url
            #     # yield Request(url=url,callback=self.parse)
            #     yield Request(url=parse.urljoin(response.url,url),callback=self.parse)

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()

    def pdf_info(self, response):
        '''获取pdf信息并持久化'''
        content = Selector(response=response).xpath('//a')
        for select_uul in content:
            url = select_uul.xpath('.//@href').extract_first()
            text = select_uul.xpath('.//text()').extract_first()
            if not url: continue
            if not text: continue
            if re.findall('.*pdf.*', url):
                if text.strip():
                    if self.md5(url) in self.url_set:
                        continue
                    else:
                        self.url_set.add(self.md5(url))
                        # href = response.url + url
                        href = self.match_url(response.url,url)
                        item_dict = {}
                        item_dict['title'] = text
                        item_dict['href'] = href
                        item_dict['md5'] = self.md5(url)
                        self.item_list.append(item_dict)
        return self.item_list

    def match_url(self,response_url,url):
        import re
        for base_url in self.start_urls:
            if re.findall('.*%s.*'%base_url,response_url):
                return base_url+url