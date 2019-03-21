import django
django.setup()
from publicsentiment import models
from kingadmin.sites import site
from kingadmin import admin_base

class UrlInfoAdmin(admin_base.AdminBase):
    list_display = ['url','key','abbreviation']
    list_filter = []
    search_fields = []



site.register(models.UrlInfo,UrlInfoAdmin)
site.register(models.WenInfo)
site.register(models.KeyWord)
