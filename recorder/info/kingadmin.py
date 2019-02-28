import django
django.setup()

from info import models

from kingadmin.sites import site
from kingadmin import admin_base

class Info_urlinfoAdmin(admin_base.AdminBase):
    list_display = ['id','key','base_url']
    list_filter = []
    search_fields = []


site.register(models.UrlInfo,Info_urlinfoAdmin)
