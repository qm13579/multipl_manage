# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
import re
import hashlib
from ..items import EuropaItem
from info.models import WebInfo,UrlInfo
# from ....models import WebInfo,UrlInfo
from urllib import parse
import sys, io,json
import requests
import jieba.analyse

import sys, io
from urllib import parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

class EurSpider(scrapy.Spider):
    name = 'eur'
    allowed_domains = ['ecb.europa.eu']
    start_urls = []
    # for obj in UrlInfo.objects.all():
    #     start_urls.append(obj.base_url)

    url_set = set()
    for obj in WebInfo.objects.all():
        url_set.add(obj.md5)

    start_urls = ['https://www.ecb.europa.eu/','http://www.treasury.gov.za','http://www.ft.com']

    def parse(self, response):
        item_list = self.pdf_info(response=response)
        for item_dict in item_list:
            item_obj = EuropaItem(
                title=item_dict['title'],
                url=item_dict['href'],
                md5=item_dict['md5'],
                keyword_1=item_dict['keyword'][0],
                keyword_2=item_dict['keyword'][1],
                keyword_3=item_dict['keyword'][2],
                keyword_4=item_dict['keyword'][3],
                keyword_5=item_dict['keyword'][4],
            )
            if  item_obj['title'] =='ENGLISH' : continue
            print('---->',item_dict['title'])
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
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()

    def pdf_info(self, response):
        '''解析网页获取url，将信息封装成字典并返回'''
        content = Selector(response=response).xpath('//a')
        item_list = []
        for i in self.start_urls:
            if re.findall('.*%s.*'%i,response.url):
                base_url=i
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
                        href = base_url + url
                        # href = response.url + url
                        href = self.match_url(response.url,url)
                        item_dict = {}
                        item_dict['title'] = text
                        item_dict['href'] = href
                        item_dict['md5'] = self.md5(url)
                        item_dict['keyword'] = self.participle(text)
                        item_list.append(item_dict)
        return item_list

    def translation(self,content):
        url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
        appid = '20170602000050620'
        secret = 'S05sDZgY7JdamCHUGFFY'
        salt = '12345678'
        hl = hashlib.md5()
        text = appid + content + salt + secret
        hl.update(text.encode('utf-8'))
        sign = hl.hexdigest()
        param = {
            'q': content,
            'from': 'en',
            'to': 'zh',
            'appid': appid,
            'salt': salt,
            'sign': sign
        }
        session = requests.session()
        session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        response = session.get(url, params=param)
        rsp = json.loads(response.text)
        text=rsp['trans_result'][0]['dst']

        msg_list=self.participle(text)
        if len(msg_list)<5:
            for i in range(5-len(msg_list)):
                msg_list.append(None)

        return msg_list

    def participle(self,content):
        '''采用结巴关键词模式进行分词,返回关键词列表'''
        msg_list=jieba.analyse.extract_tags(content,topK=5)
        if len(msg_list)<5:
            for i in range(5-len(msg_list)):
                msg_list.append( '')
        return msg_list

    def match_url(self,response_url,url):
        import re
        for base_url in self.start_urls:
            if re.findall('.*%s.*'%base_url,response_url):
                return base_url+url
