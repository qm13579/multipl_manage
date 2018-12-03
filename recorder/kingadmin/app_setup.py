import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")

from django.conf import settings

for apps in settings.INSTALLED_APPS:
    try:
        print('%s.kingadmin'%apps)
        mon=__import__('%s.kingadmin'%apps)
    except Exception as e:
        print(e)

# from kingadmin.sites import site
# print(site.enble_admin)