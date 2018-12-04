from django.conf.urls import url,include
from django.contrib import admin
from kingadmin import views

urlpatterns = [
    url(r'^$',views.home),
    url(r'^(\w+)/(\w+)$',views.app_table,name='appname'),

]