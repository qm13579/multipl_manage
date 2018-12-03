from django.shortcuts import render
from app01 import models
#django 登录验证
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    return render(request,'home/home.html')