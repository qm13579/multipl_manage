# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
import re
import sys,io
from ..items import EuropaItem
from info.models import WebInfo,UrlInfo
from urllib import parse

class EurSpider(scrapy.Spider):
    name = 'eur'
    allowed_domains = ['ecb.europa.eu']
    start_urls = []
    for obj in UrlInfo.objects.all():
        start_urls.append(obj.base_url)
    url_set = set()
    for obj in WebInfo.objects.all():
        url_set.add(obj.md5)
    def parse(self, response):
        print('--------->',response.url)
        item_list = self.pdf_info(response=response)
        # for item_dict in item_list:
        #     item_obj = EuropaItem(
        #         title=item_dict['title'],
        #         url=item_dict['href'],
        #         md5=item_dict['md5']
        #     )
        #     yield item_obj
        #     持久化url
        content = Selector(response=response).xpath('//a/@href').extract()
        for url in content:
            if len(url) < 2 :continue
            elif  not url.startswith('/') : continue
            elif url[1] == '/':continue
            url=parse.urljoin(response.url,url)
            yield Request(url=url,callback=self.parse)
    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()

    def pdf_info(self, response):
        '''获取pdf信息并持久化'''
        content = Selector(response=response).xpath('//a')
        item_list = []
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
                        href = self.start_urls[0] + url
                        item_dict = {}
                        item_dict['title'] = text
                        item_dict['href'] = href
                        item_dict['md5'] = self.md5(url)
                        item_list.append(item_dict)
        return item_list
