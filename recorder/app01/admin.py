from django.contrib import admin

# Register your models here.
from app01 import models

admin.site.register(models.UserProfile)
admin.site.register(models.DepartmentGroup)
admin.site.register(models.FileStore)
admin.site.register(models.Standard)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.Summary)