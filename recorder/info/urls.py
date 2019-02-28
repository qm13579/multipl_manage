from django.conf.urls import url,include
from django.contrib import admin
from info import views
urlpatterns = [
    url(r'^$',views.scrapy_info),
    url(r'^info/$',views.scrapy_url_info,name='scrapy_url_info'),
]
