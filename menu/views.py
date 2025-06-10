from django.shortcuts import render

# Create your views here.
from .models import Menu
# Views for the menu app

def menu_list(request):
    menu_list = Menu.objects.all()

    return render(request, 'menu/list.html', {'menu_list': menu_list})



def menu_detail(request, slug):
    pass