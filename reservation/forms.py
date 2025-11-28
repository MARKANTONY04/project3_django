

from django import forms
from .models import Reservation
from .utils import SLOT_STARTS, is_table_available
from django.core.exceptions import ValidationError
from datetime import date, datetime

# build time choices once
TIME_CHOICES = [(t.strftime("%H:%M"), t.strftime("%I:%M %p")) for t in SLOT_STARTS]

class ReservationForm(forms.ModelForm):
    # explicit time field so both create & edit use the same widget/value format
    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Reservation Time",
    )

    class Meta:
        model = Reservation
        exclude = ["user"]           # time is provided above
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
        chosen_date = self.cleaned_data.get("date")
        if chosen_date and chosen_date < date.today():
            raise ValidationError("You cannot make a reservation in the past.")
        return chosen_date

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get("number_of_guests")
        if guests is None:
            raise ValidationError("Please enter number of guests.")
        if guests < 1 or guests > 10:
            raise ValidationError("Guests must be between 1 and 10.")
        return guests

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def clean(self):
        cleaned = super().clean()
        date_val = cleaned.get("date")
        time_str = cleaned.get("time")   # from the ChoiceField, e.g. "14:00"
        guests = cleaned.get("number_of_guests")

        # basic presence checks; field-specific errors will show as well
        if not date_val or not time_str or not guests:
            return cleaned

        # convert time string to time object
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValidationError("Invalid time selected.")

        # availability check (exclude current instance if editing)
        exclude_id = getattr(self.instance, "pk", None)
        if not is_table_available(date_val, time_obj, guests, exclude_id=exclude_id):
            raise ValidationError("Sorry, the restaurant is fully booked for this timeslot.")

        # store time_obj into cleaned so save() gets proper object
        cleaned["time"] = time_obj
        return cleaned


# EditReservationForm can reuse ReservationForm (no change needed)
class EditReservationForm(ReservationForm):
    pass

