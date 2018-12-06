from django.shortcuts import render

# Create your views here.
from kingadmin.sites import site
from kingadmin import app_setup
from django.contrib.auth.decorators import login_required
app_setup.kingadmin_auto_discover()
print (site.enble_admin)


@login_required
def home(request):

    class_admin = site.enble_admin

    return render(request,'home.html',locals())


def sort_queryset(request,queryset,class_admin):
    order=request.GET.get('o')
    # print('---->',v)
    if order:
        field = class_admin.list_display[abs(int(order)) - 1]
        if '-' in order:
            queryset=queryset.order_by('-%s'%field)
        else:
            queryset=queryset.order_by(field)

    return queryset,order
def filter_queryset(request,queryset,class_admin):
    filter_dict={}
    for key,val in request.GET.items():
        print(key,val)
        if key not in ['o']:
            if val:
                filter_dict[key]=val

    queryset=queryset.filter(**filter_dict)

    return queryset,filter_dict

@login_required
def app_table(request,app_name,table_name):

    class_admin = site.enble_admin[app_name][table_name]

    queryset=class_admin.model.objects.all()

    #排序
    queryset,order=sort_queryset(request,queryset,class_admin)
    #筛选
    queryset,filter_dict=filter_queryset(request,queryset,class_admin)

    return  render(request,'app_table.html',locals())