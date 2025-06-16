from django.db import models

# Create your models here.

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()

    def __str__(self):
        return f"Booking confirmed. Reservation for {self.name} on {self.date} at {self.time}. We look forward to seeing you."