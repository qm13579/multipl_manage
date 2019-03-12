from django.shortcuts import render

# Create your views here.



def PublicSentiment(request):



    return render(request,'PublicSentiment/PublicSentiment.html',locals())