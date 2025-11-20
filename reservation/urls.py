# from django.urls import path
# from . import views

# URL configuration for the menu app

# app_name = 'reservation'

# The urlpatterns list routes URLs to views in the menu app.

# urlpatterns = [
#     path('', views.reservation_view, name='reservation_view'),
#     path("book/", create_reservation, name="create_reservation"),
#     
# ]


from django.urls import path
from .views import (
    create_reservation,
    reservation_list,
    edit_reservation,
    delete_reservation,
)

# URL configuration for the menu app

app_name = 'reservation'

# The urlpatterns list routes URLs to views in the menu app.

urlpatterns = [
    path("book/", create_reservation, name="create_reservation"),
    path("my-reservations/", reservation_list, name="reservation_list"),
    path("edit/<int:pk>/", edit_reservation, name="edit_reservation"),
    path("delete/<int:pk>/", delete_reservation, name="delete_reservation"),
]
