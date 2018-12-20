from django.shortcuts import render,redirect
from info import models
# Create your views here.

def scrapy_info(request):

    admin=models.WebInfo.objects.all()

    return render(request,'scrapy/ScrapyInfo.html',locals())