# chat gpt helped recreate this file from previous iteration to fit with the new app

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse


from .models import Reservation
from .forms import ReservationForm
from .utils import is_table_available, SLOT_STARTS
from datetime import datetime
from .forms import EditReservationForm

@login_required
def create_reservation(request):
    if request.method == "POST":

        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # FIX: properly convert time string to a real Python time object
            slot_str = request.POST.get("time")  # e.g. "14:00"
            reservation.time = datetime.strptime(slot_str, "%H:%M").time()

            # availability check
            if not is_table_available(reservation.date, reservation.time, reservation.number_of_guests):
                messages.error(request, "No tables available for this slot. Please choose another time or date.")
                return render(request, "reservation/reservation.html", {"form": form, "time_slots": SLOT_STARTS})

            reservation.save()

            messages.success(request, "Reservation created successfully.")
            return redirect("reservation:reservation_success", pk=reservation.pk)

    else:
        form = ReservationForm()

    return render(request, "reservation/reservation.html", {"form": form, "time_slots": SLOT_STARTS})



@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user).order_by("date", "time")
    return render(request, "reservation/reservation_list.html", {"reservations": reservations})




@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated = form.save(commit=False)

            # manually convert string to time if needed
            if isinstance(updated.time, str):
                from datetime import datetime
                updated.time = datetime.strptime(updated.time, "%H:%M").time()

            # availability check remains the same...
            # (existing code)
            
            updated.save()
            messages.success(request, "Reservation updated.")
            return redirect("reservation:reservation_list")
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, "reservation/edit_reservation.html", {"form": form, "reservation": reservation})


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
    """
    AJAX endpoint:
    GET params: date=YYYY-MM-DD, time=HH:MM, guests=int
    returns JSON: {"available": true/false, "message": "..."}
    """
    date_str = request.GET.get("date")
    time_str = request.GET.get("time")
    guests = request.GET.get("guests")

    if not date_str or not time_str or not guests:
        return JsonResponse({"available": False, "message": "Missing parameters."})

    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        # allow times like "12:00" or "12:00:00"
        time_parts = [int(p) for p in time_str.split(":")]
        time_obj = __import__("datetime").time(time_parts[0], time_parts[1])
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
