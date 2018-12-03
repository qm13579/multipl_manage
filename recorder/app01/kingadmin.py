
import django
django.setup()

from app01 import models
from kingadmin.sites import site

site.register(models.UserProfile)
site.register(models.Summary)
site.register(models.Detailed)
