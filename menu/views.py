from django.shortcuts import render

# Create your views here.
from .models import Menu , Category
# Views for the menu app

def menu_list(request):
    menu_list = Menu.objects.all()
    categories = Category.objects.all()
    context = {
        'menu_list': menu_list,
        'categories': categories,
    }

    return render(request, 'menu/list.html',  context)



def menu_detail(request, slug):
    menu_detail = Menu.objects.get(slug=slug)

    context = {'menu_detail': menu_detail}

    return render(request , 'menu/detail.html' , context)