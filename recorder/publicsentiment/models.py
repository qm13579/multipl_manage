from django.db import models

# Create your models here.


class UrlInfo(models.Model):
    '''url_name,verbosr_name'''
    url=models.URLField(verbose_name='网址')
    key=models.CharField(max_length=128,verbose_name='名称')
    abbreviation=models.CharField(max_length=64,verbose_name='缩写')
    def __str__(self):
        return self.key
class WenInfo(models.Model):
    title = models.CharField(max_length=126,verbose_name='标题')
    url = models.CharField(max_length=126,verbose_name='链接')
    url_md5 = models.CharField(max_length=64,verbose_name='URL哈希化')
    url_info=models.ForeignKey('UrlInfo',on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
class KeyWord(models.Model):
    key = models.CharField(max_length=32)
    content = models.ManyToManyField('WenInfo')

    def __str__(self):
        return self.key