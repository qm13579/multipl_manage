from django.db import models

# Create your models here.


class UrlInfo(models.Model):
    '''url_name,verbosr_name'''
    url=models.URLField(verbose_name='网址')
    key=models.CharField(max_length=128,verbose_name='名称')
    abbreviation=models.CharField(max_length=64,verbose_name='缩写')

    def __str__(self):
        return self.key
