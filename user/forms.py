from django import forms
from user.models import userreg,Booking

class userregform(forms.ModelForm):
    class Meta:
        model=userreg
        fields="__all__"

class bookingform(forms.ModelForm):
    class Meta:
        model=Booking
        fields=[
            'service_description',
            'service_address',
            'contact_number',
            'booking_date',
            'booking_time',
        ]