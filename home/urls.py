from django.urls import path
from . import views

# URL configuration for the home app

app_name = 'home'

# The urlpatterns list routes URLs to views in the home app.

urlpatterns = [
    path('', views.home_view, name='home_view'),
]