import sys, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")
import django
django.setup()

from info import models