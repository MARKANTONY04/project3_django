from django import forms
from .models import Reservation
import datetime

TIME_SLOTS = [
    (datetime.time(12, 0), "12:00"),
    (datetime.time(14, 0), "14:00"),
    (datetime.time(16, 0), "16:00"),
    (datetime.time(18, 0), "18:00"),
    (datetime.time(20, 0), "20:00"),
]

class ReservationForm(forms.ModelForm):
    time = forms.ChoiceField(choices=[(t.isoformat(), label) for t, label in TIME_SLOTS])

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'email', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            # time will be a select via ChoiceField above
        }
        labels = {
            'name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'date': 'Reservation Date',
            'time': 'Reservation Time',
            'number_of_guests': 'Number of Guests',
        }

    # below functions added with chat gpt help
    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests is None:
            raise forms.ValidationError("Please enter number of guests.")
        if guests < 1 or guests > 10:
            raise forms.ValidationError("Guests must be between 1 and 10.")
        return guests

    def clean_time(self):
        time_str = self.cleaned_data.get('time')
        # time_str is ISO format like '12:00:00' or '12:00'
        try:
            # convert to time object
            if isinstance(time_str, str):
                parts = [int(p) for p in time_str.split(":")]
                return datetime.time(parts[0], parts[1])
            return time_str
        except Exception:
            raise forms.ValidationError("Select a valid time slot.")
