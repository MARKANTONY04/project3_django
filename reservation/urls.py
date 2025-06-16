from django.urls import path
from . import views

# URL configuration for the menu app

app_name = 'reservation'

# The urlpatterns list routes URLs to views in the menu app.

urlpatterns = [
    path('', views.reservation_view, name='reservation_view'),
]