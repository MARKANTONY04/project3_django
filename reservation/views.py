from .models import Reservation
from django.shortcuts import render
from .forms import ReservationForm

# Create your views here.
from reservation.models import Reservation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

from .models import Reservation
from .forms import ReservationForm

def reservation_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_guests = request.POST.get('number_of_guests')

        reservation = Reservation(
            name=name,
            phone_number=phone_number,
            email=email,
            date=date,
            time=time,
            number_of_guests=number_of_guests
        )
        reservation.save()

        return render(request, 'reservation/success.html', {'reservation': reservation})

    return render(request, 'reservation/reservation.html')


# chat gpt helped create this function

@login_required
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # Determine table-size group
            group = reservation.table_group()

            # Count existing reservations for same group + date + time
            existing = Reservation.objects.filter(
                date=reservation.date,
                time=reservation.time,
                number_of_guests__lte=group,
                number_of_guests__gt=group/2    # Ensures they are in same capacity group
            ).count()

            if existing >= 3:
                messages.error(request, "No tables available for this time slot.")
                return render(request, "create_reservation.html", {"form": form})

            reservation.save()

            # ---- Email Confirmation ----
            send_mail(
                subject="Your Reservation Confirmation",
                message=f"Hi {reservation.name}, your booking for {reservation.date} at {reservation.time} is confirmed!",
                from_email="noreply@example.com",
                recipient_list=[reservation.email],
                fail_silently=True,
            )

            messages.success(request, "Reservation created successfully!")
            return redirect("reservation_list")

    else:
        form = ReservationForm()

    return render(request, "create_reservation.html", {"form": form})


