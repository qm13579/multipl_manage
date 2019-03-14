
from django.conf.urls import url,include
from django.contrib import admin
from publicsentiment import views
urlpatterns = [
    url(r'^$', views.PublicSentiment),
    url(r'^urlinfo/$', views.PublicSentiment_urlinfo),
]