from django.shortcuts import render,redirect

# Create your views here.
from kingadmin.sites import site
from kingadmin import app_setup
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from kingadmin.modelform import create_model_from
app_setup.kingadmin_auto_discover()
print (site.enble_admin)


@login_required
def home(request):

    class_admin = site.enble_admin

    return render(request,'home.html',locals())


def sort_queryset(request,queryset,class_admin):
    '''排序'''
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
    '''筛选'''
    filter_dict={}
    for key,val in request.GET.items():
        print(key,val)
        if key not in ['o','q','page']:
            if val:
                filter_dict[key]=val

    queryset=queryset.filter(**filter_dict)

    return queryset,filter_dict
def seach_queryest(request,queryset,class_admin):
    q=request.GET.get('q')
    if q:
        from django.db.models import Q
        q1=Q()
        for search_fields in class_admin.search_fields:
            q2=Q()
            q2.connector='OR'
            q2.children.append((search_fields,q))
            q1.add(q2,'OR')
        return queryset.filter(q1)

    else:
        return queryset

@login_required
def app_table(request,app_name,table_name):

    class_admin = site.enble_admin[app_name][table_name]

    queryset=class_admin.model.objects.all()
    #排序
    queryset,order=sort_queryset(request,queryset,class_admin)
    #筛选
    queryset,filter_dict=filter_queryset(request,queryset,class_admin)
    #搜索
    queryset=seach_queryest(request,queryset,class_admin)
    #分页
    paginator = Paginator(queryset, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return  render(request,'app_table.html',locals())
def table_change(request,app_name,table_name,uid):
    class_admin = site.enble_admin[app_name][table_name]
    obj=class_admin.model.objects.get(id=uid)
    form=create_model_from(class_admin)
    if request.method == 'GET':
        form_obj=form(instance=obj)
    else:
        form_obj=form(instance=obj,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s'%(app_name,table_name))
    return render(request,'table_change.html',locals())

def table_delete(request,app_name,table_name,uid):

    return render(request,'table_delete.html',locals())