from django import forms
from .models import Reservation
from .utils import SLOT_STARTS

from django.core.exceptions import ValidationError
from datetime import date


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        # remove "time" because we supply our own dropdown in the template
        exclude = ["user", "time"]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def clean_date(self):
        chosen_date = self.cleaned_data["date"]
        if chosen_date < date.today():
            raise ValidationError("You cannot make a reservation in the past.")
        return chosen_date


    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests is None:
            raise forms.ValidationError("Please enter number of guests.")
        if guests < 1 or guests > 10:
            raise forms.ValidationError("Guests must be between 1 and 10.")
        return guests


# here edit reservation form time

# forms.py

class EditReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ["user"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.Select(attrs={"class": "form-control"}, choices=[(t, t.strftime("%H:%M")) for t in SLOT_STARTS]),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def clean_date(self):
        chosen_date = self.cleaned_data["date"]
        if chosen_date < date.today():
            raise ValidationError("You cannot make a reservation in the past.")
        return chosen_date

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get("number_of_guests")
        if guests is None:
            raise forms.ValidationError("Please enter number of guests.")
        if guests < 1 or guests > 10:
            raise forms.ValidationError("Guests must be between 1 and 10.")
        return guests


