import django
django.setup()

from app01 import models
from kingadmin.sites import site
from kingadmin import admin_base

class SummaryAdmin(admin_base.AdminBase):
    list_display = ['id','user','lack_count','file_stores_id']
    list_filter = ['file_stores_id']
    search_fields = ['id']
class FileStoreAdmin(admin_base.AdminBase):
    list_display = ['file_addre','file_time','file_format']

site.register(models.UserProfile)
site.register(models.Summary,SummaryAdmin)
site.register(models.Detailed)
site.register(models.FileStore,FileStoreAdmin)
