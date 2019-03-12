import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")

from django.conf import settings

def kingadmin_auto_discover():
    for apps in settings.INSTALLED_APPS:
        try:
            mon=__import__('%s.kingadmin'%apps)
            print('%s.kingadmin'%apps)
        except Exception as e:
            pass