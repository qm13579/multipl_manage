from django.conf.urls import url,include
from django.contrib import admin
from kingadmin import views

urlpatterns = [
    url(r'^$',views.home),
    url(r'^(\w+)/(\w+)$',views.app_table,name='appname'),
    url(r'^(\w+)/(\w+)/(\d+)/change$',views.table_change,name='change'),
    url(r'^(\w+)/(\w+)/(\d+)/delete$',views.table_delete,name='delete'),

]