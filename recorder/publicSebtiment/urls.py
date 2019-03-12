
from django.conf.urls import url,include
from django.contrib import admin
from publicSebtiment import views
urlpatterns = [

    url(r'^$', views.PublicSentiment),
]