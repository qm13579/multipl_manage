from django.shortcuts import render
from publicsentiment import models
# Create your views here.



def PublicSentiment(request):

    return render(request,'PublicSentiment/PublicSentiment.html',locals())

def PublicSentiment_urlinfo(request):

    queryset=models.UrlInfo.objects.all()

    return render(request,'PublicSentiment/PublicSentiment_urlinfo.html',locals())