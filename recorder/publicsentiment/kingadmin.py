import django
django.setup()
from publicsentiment import models
from kingadmin.sites import site
from kingadmin import admin_base


class UrlAdmin(admin_base.AdminBase):
    pass



site.register(models.UrlInfo)
