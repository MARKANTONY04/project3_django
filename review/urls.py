from django.urls import path
from . import views

# URL configuration for the review app

app_name = 'review'

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('', views.reviews_list, name='reviews_list'),
]
