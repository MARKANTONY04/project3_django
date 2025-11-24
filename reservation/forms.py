from django import forms
from .models import Reservation
from .utils import SLOT_STARTS

class ReservationForm(forms.ModelForm):
    # Match the template/time slot system: use "HH:MM" strings for choices
    time = forms.TimeField(
        widget=forms.Select(
            choices=[(t.strftime("%H:%M"), t.strftime("%H:%M")) for t in SLOT_STARTS]
        )
    )

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'email', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1})
        }
        labels = {
            'name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'date': 'Reservation Date',
            'time': 'Reservation Time',
            'number_of_guests': 'Number of Guests',
        }

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests is None:
            raise forms.ValidationError("Please enter number of guests.")
        if guests < 1 or guests > 10:
            raise forms.ValidationError("Guests must be between 1 and 10.")
        return guests
