from django.urls import resolve
from django.shortcuts import render,redirect,HttpResponse
from kingadmin.permissions_list import Permission_dict
from django.conf import settings

def per(*args,**kwargs):
    '''权限控制'''
    request=args[0]
    resolve_url_obj=resolve(request.path)
    resolve_url_name=resolve_url_obj.url_name
    match_results = [None,]
    match_key = None
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    for per_key,per_val in Permission_dict.items():
        per_url_name=per_val[0]
        per_method=per_val[1]
        per_args=per_val[2]
        per_kwargs=per_val[3]
        per_hook_func=per_val[4] if len(per_val)>4 else None
        args_matched=False
        if per_url_name == resolve_url_name:
            if per_method == request.method:
                for item in per_args:
                    request_method_func=getattr(request,per_method)
                    if request_method_func.get(item,None):
                        args_matched = True
                    else:
                        args_matched=False
                        break
                else:
                    args_matched=True
                kwargs_mtched=False
                for key,val in per_kwargs.items():
                    request_method_func=getattr(request,per_method)
                    arg_val = request_method_func.get(key)
                    if arg_val == str(val):
                        kwargs_mtched = True
                    else:
                        args_matched = False
                        break
                else:
                    kwargs_mtched = True
                match_results=[args_matched,kwargs_mtched]
                if all(match_results):
                    match_key=per_key
                    break
    if all(match_results):
        '''app01_table_list'''
        app_name,*per_name=match_key.split('_')
        perm_obj='%s.%s' % (app_name,match_key)
        print('perm_obj:',perm_obj,request.user,'--->',request.user.has_perm(perm_obj))
        if request.user.has_perm(perm_obj):
            print('用户有此权限')
            return True
        else:
            return False
    else:
        print('未检测到用户权限')
def check_permissions(func):
    '''检查权限'''
    def inner(*args,**kwargs):
        if  not per(*args,**kwargs):
            request=args[0]
            return render(request,'403.html')
        return func(*args,**kwargs)
    return inner
