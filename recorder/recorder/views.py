from django.shortcuts import render,redirect
#django 登录判断
from django.contrib.auth.decorators import login_required
#django 登录验证
from django.contrib.auth import authenticate,login,logout
def acc_login(request):
    error_msg=''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        print (user)
        if user:
            print ('验证成功')
            login(request,user)#发送一个session
            return redirect(request.GET.get('next','/home'))
        else:
            error_msg='Wrong user or password'
    return render(request,'login.html',{'error_msg':error_msg})

def acc_logout(request):
    logout(request)
    return redirect('/login')