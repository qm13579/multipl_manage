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
    # print('get_order',order)
    if order:
        field = class_admin.list_display[abs(int(order)) - 1]
        if '-' in order:
            queryset=queryset.order_by('-%s'%field)
            print('order',order,type(order))
        else:
            queryset=queryset.order_by(field)

    return queryset,order

@login_required
def app_table(request,app_name,table_name):

    class_admin = site.enble_admin[app_name][table_name]
    querset=class_admin.model.objects.all()

    #排序
    querset,order=sort_queryset(request,querset,class_admin)

    return  render(request,'app_table.html',locals())