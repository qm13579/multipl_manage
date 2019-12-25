#爬虫内容解析
from scrapy.selector import Selector
import re
from info.removal import SpiderRemoval
from info.models import UrlInfo
class analysisSpider:
    def __init__(self):
        self.sr = SpiderRemoval()

    def herfCommonAnalysis(self,startUrl,response,urlsSet,participle):
        """
        :param startUrl: 网站站点
        :param response: spider的下载内容
        :param urlsSet: url集合，在spider生成
        :param participle: 分词
        :return: list包含有 data list
        """
        print("SUCCESS URL:",response.url)
        # 获取所有A标签
        content = Selector(response=response).xpath('//a')
        item_list = []
        #每一个标签获取href和内容
        for select_uul in content:
            url = select_uul.xpath('.//@href').extract_first()
            text = select_uul.xpath('.//text()').extract_first()
            if not url: continue
            if not text: continue
            if re.findall('.*pdf.*', url):
                if text.strip():
                    if self.sr.MD5(url) in urlsSet:
                        continue
                    else:
                        urlsSet.add(self.sr.MD5(url))
                        base_url_id = UrlInfo.objects.get(base_url=startUrl).id
                        item_dict = {}
                        item_dict['title'] = text
                        item_dict['href'] = response.url+url  #startUrl+url
                        item_dict['md5'] = self.sr.MD5(url)
                        item_dict['base_url_id'] = base_url_id
                        item_dict['keyword'] = participle(text)
                        item_list.append(item_dict)
        return item_list
