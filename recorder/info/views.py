from django.shortcuts import render,redirect
from info import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def search_func(queryset,search):
    print('---->', search)
    from django.db.models import Q
    q1 = Q()
    for search_file in ['keyword_1','keyword_2','keyword_3','keyword_4','keyword_5']:
        q2=Q()
        q2.connector = 'OR'
        q2.children.append((search_file,search))
        q1.add(q2,'OR')
    return queryset.filter(q1)

def scrapy_info(request):

    queryset=models.WebInfo.objects.all().order_by('-date')

    if request.method == 'GET':
        search=request.GET.get('s')
        if search:
            queryset = search_func(queryset,search)


    paginator = Paginator(queryset, 10)  # Show 20 contacts per page
    page = request.GET.get('page')

    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    #获取当前时间,传入前端
    import time
    time_stamp=time.localtime()
    current_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render(request,'scrapy/ScrapyInfo.html',locals())

def scrapy_url_info(request):
    from info import models
    queryset=models.UrlInfo.objects.all()
    #把实例传入前端，进行 # 增删改查
    return render(request,'scrapy/ScrapyUrl.html',locals())
