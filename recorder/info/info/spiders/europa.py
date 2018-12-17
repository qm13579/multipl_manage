# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
import re
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class EuropaSpider(scrapy.Spider):
    name = 'europa'
    allowed_domains = ['ecb.europa.eu']
    start_urls = ['https://www.ecb.europa.eu/']
    url_set=set()
    def parse(self, response):

        self.pdf_info(response=response)

        # 持久化url
        content = Selector(response=response).xpath('//a/@href').extract()
        for url in content:
            if len(url) < 2 :continue
            elif  not url.startswith('/') : continue
            elif url[1] == '/':continue
            url=self.start_urls[0]+url
            yield Request(url=url,callback=self.parse)
    def md5(self,url):
        import hashlib
        obj=hashlib.md5()
        obj.update(bytes(url,encoding='utf-8'))
        return obj.hexdigest()
    def pdf_info(self,response):
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
                        print(self.start_urls[0] + url)