from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'email', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'date': 'Reservation Date',
            'time': 'Reservation Time',
            'number_of_guests': 'Number of Guests',
        }