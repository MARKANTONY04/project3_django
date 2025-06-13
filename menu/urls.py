from django.urls import path
from . import views

# URL configuration for the menu app

app_name = 'menu'

# The urlpatterns list routes URLs to views in the menu app.

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<slug:slug>' , views.menu_detail, name='menu_detail'),
]