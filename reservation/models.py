# from django.db import models

# Create your models here.

# class Reservation(models.Model):
#     name = models.CharField(max_length=50)
#     phone_number = models.IntegerField()
#     email = models.EmailField()
#     date = models.DateField()
#     time = models.TimeField()
#     number_of_guests = models.PositiveIntegerField()

#     def __str__(self):
#         return f"Booking confirmed. Reservation for {self.name} on {self.date} at {self.time}. We look forward to seeing you."

# chat gpt helped with this new version of reservation/models.py

from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()

    TABLE_SIZES = [2, 4, 6, 8, 10]

    def table_group(self):
        """
        Returns capacity group based on number of guests.
        """
        for size in self.TABLE_SIZES:
            if self.number_of_guests <= size:
                return size
        return 10

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"