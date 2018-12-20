from django.db import models

# Create your models here.


class WebInfo(models.Model):
    title=models.CharField(max_length=248,verbose_name='标题')
    url = models.CharField(max_length=248,verbose_name='链接')
    md5=models.CharField(max_length=128,verbose_name='链接哈希化')
    date=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    base_url=models.ForeignKey('UrlInfo',blank=True,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.md5

class UrlInfo(models.Model):
    base_url=models.CharField(max_length=128,verbose_name='根')
    key=models.CharField(max_length=248,verbose_name='提取关键词')
    def __str__(self):
        return self.base_url