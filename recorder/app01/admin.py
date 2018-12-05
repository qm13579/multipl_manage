from django.contrib import admin

# Register your models here.
from app01 import models
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('user','lack_count','file_stores_id')

admin.site.register(models.UserProfile)
admin.site.register(models.DepartmentGroup)
admin.site.register(models.FileStore)
admin.site.register(models.Standard)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.Summary,SummaryAdmin)
admin.site.register(models.Detailed)