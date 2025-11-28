# chat gpt helped recreate this file from previous iteration to fit with the new app

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import Reservation
from .forms import ReservationForm, EditReservationForm
from .utils import is_table_available, SLOT_STARTS

@login_required
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Reservation created successfully.")
            return redirect("reservation:reservation_success", pk=reservation.pk)
        # if form invalid, it will re-render and display form.non_field_errors
    else:
        form = ReservationForm()

    return render(request, "reservation/reservation.html", {"form": form, "time_slots": SLOT_STARTS})


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation updated successfully.")
            return redirect("reservation:reservation_list")
    else:
        # prepare initial time selection as HH:MM string so the ChoiceField preselects it
        initial = {"time": reservation.time.strftime("%H:%M")}
        form = EditReservationForm(instance=reservation, initial=initial)

    return render(request, "reservation/edit_reservation.html", {"form": form, "reservation": reservation, "time_slots": SLOT_STARTS})


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user).order_by("date", "time")
    return render(request, "reservation/reservation_list.html", {"reservations": reservations})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation deleted.")
        return redirect("reservation:reservation_list")
    return render(request, "reservation/delete_reservation.html", {"reservation": reservation})


@login_required
def check_availability(request):
    date_str = request.GET.get("date")
    time_str = request.GET.get("time")
    guests = request.GET.get("guests")

    if not date_str or not time_str or not guests:
        return JsonResponse({"available": False, "message": "Missing parameters."})

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        guests = int(guests)
    except Exception:
        return JsonResponse({"available": False, "message": "Invalid parameters."})

    available = is_table_available(date_obj, time_obj, guests)
    msg = "Available" if available else "Fully booked"
    return JsonResponse({"available": available, "message": msg})


@login_required
def reservation_success(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    return render(request, "reservation/success.html", {"reservation": reservation})

