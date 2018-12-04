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

def app_table(request,app_name,table_name):
    class_admin = site.enble_admin[app_name][table_name]
    print(class_admin)
    querset=class_admin.objects.all()
    return  render(request,'app_table.html',locals())