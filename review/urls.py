from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

# URL configuration for the review app

app_name = 'review'

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('', views.reviews_list, name='reviews_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

