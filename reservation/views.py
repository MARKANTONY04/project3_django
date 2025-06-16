from .models import Reservation
from django.shortcuts import render

# Create your views here.
from reservation.models import Reservation

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

    return render(request, 'reservation/reservation_form.html')