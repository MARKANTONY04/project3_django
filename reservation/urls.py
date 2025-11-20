from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path("book/", views.create_reservation, name="create_reservation"),
    path("my-reservations/", views.reservation_list, name="reservation_list"),
    path("edit/<int:pk>/", views.edit_reservation, name="edit_reservation"),
    path("delete/<int:pk>/", views.delete_reservation, name="delete_reservation"),
    path("check-availability/", views.check_availability, name="check_availability"),
]
