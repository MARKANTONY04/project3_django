from .models import Reservation

def is_table_available(date, time, guests):
    if guests <= 2:
        group = 2
    elif guests <= 4:
        group = 4
    elif guests <= 6:
        group = 6
    elif guests <= 8:
        group = 8
    else:
        group = 10

    existing = Reservation.objects.filter(
        date=date,
        time=time,
        number_of_guests__lte=group,
        number_of_guests__gte=group - 1,
    ).count()

    return existing < 3