#spider去重
import hashlib
from info.models import UrlInfo,WebInfo
class SpiderRemoval:

    def __init__(self):
        pass
    def MD5(self,url):
        """
        :param url:链接
        :return: url的MD5形式
        """
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()

    def urlSet(self,start_urls):
        """
        :param start_urls:传入spider的star_urls type:list
        :return: urlSet,当前startUrl的所有已存在的MD5
        """
        print("start_url:", start_urls)
        url_id = UrlInfo.objects.get(base_url=start_urls[0]).id
        url_set = set()
        for obj in WebInfo.objects.filter(base_url=url_id):
            url_set.add(obj.md5)
        return url_set