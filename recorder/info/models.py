from django.db import models

# Create your models here.


class WebInfo(models.Model):
    title=models.CharField(max_length=248,verbose_name='标题')
    url = models.CharField(max_length=248,verbose_name='链接')
    md5=models.CharField(max_length=128,verbose_name='链接哈希化')
    date=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    def __str__(self):
        return self.title