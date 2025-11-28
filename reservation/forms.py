

from django import forms
from .models import Reservation
from .utils import SLOT_STARTS
from django.core.exceptions import ValidationError
from datetime import date

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ["user", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "pattern": "[0-9]+",
                "inputmode": "numeric",
                "placeholder": "Digits only"
            }),
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
        if guests < 1 or guests > 10:
            raise ValidationError("Guests must be between 1 and 10.")
        return guests

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone


class EditReservationForm(ReservationForm):
    """Same as ReservationForm but includes time dropdown."""
    time = forms.ChoiceField(
        choices=[(t.strftime("%H:%M"), t.strftime("%I:%M %p")) for t in SLOT_STARTS],
        widget=forms.Select(attrs={"class": "form-control"})
    )

