from django.shortcuts import render,redirect
from info import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def scrapy_info(request):

    queryset=models.WebInfo.objects.all().order_by('-date')

    paginator = Paginator(queryset, 10)  # Show 20 contacts per page
    page = request.GET.get('page')

    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return render(request,'scrapy/ScrapyInfo.html',locals())