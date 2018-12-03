from django.shortcuts import render

# Create your views here.
from kingadmin.sites import site
from kingadmin import app_setup
app_setup.kingadmin_auto_discover()
print (site.enble_admin)



def home(request):

    return render(request,'home.html')