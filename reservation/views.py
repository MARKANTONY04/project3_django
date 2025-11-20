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

@login_required
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # availability check
            if not is_table_available(reservation.date, reservation.time, reservation.number_of_guests):
                messages.error(request, "No tables available for this slot. Please choose another time or date.")
                return render(request, "reservation/reservation.html", {"form": form, "time_slots": SLOT_STARTS})

            reservation.save()

            # send confirmation email (requires EMAIL_* config in settings)
            try:
                send_mail(
                    subject="Reservation Confirmed - Barney's Bistro",
                    message=f"Hi {reservation.name},\n\nYour reservation for {reservation.date} at {reservation.time} for {reservation.number_of_guests} guest(s) is confirmed.\n\nThank you!",
                    from_email=None,  # uses DEFAULT_FROM_EMAIL if configured
                    recipient_list=[reservation.email],
                    fail_silently=True,
                )
            except Exception:
                # fail silently in production; message to user already shown
                pass

            messages.success(request, "Reservation created successfully.")
            return redirect("reservation:reservation_list")
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
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated = form.save(commit=False)

            # check availability; allow saving if the reservation is unchanged or if there's room
            # exclude current reservation from overlap count by temporarily deleting it from DB check
            reservation_id = reservation.id
            # Temporarily ignore current record by filtering in utils with a small change:
            # We'll do manual check here: compute overlap count excluding this id.
            from datetime import datetime, timedelta
            req_start = datetime.combine(updated.date, updated.time)
            req_end = req_start + timedelta(hours=2)

            # compute group
            group = updated.table_group()

            existing_qs = Reservation.objects.filter(date=updated.date).exclude(pk=reservation_id)
            overlapping_count = 0
            for r in existing_qs:
                r_start = datetime.combine(r.date, r.time)
                r_end = r_start + timedelta(hours=2)
                if r.table_group() == group and req_start < r_end and r_start < req_end:
                    overlapping_count += 1

            if overlapping_count >= 3:
                messages.error(request, "No tables available for the updated slot.")
                return render(request, "reservation/edit_reservation.html", {"form": form, "reservation": reservation})

            updated.save()
            messages.success(request, "Reservation updated.")
            return redirect("reservation:reservation_list")
    else:
        form = ReservationForm(instance=reservation)

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
