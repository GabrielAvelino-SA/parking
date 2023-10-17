from django import forms
from parking.models import Reservation
from django.core.validators import RegexValidator
from re import search


class FormReservation(forms.Form):
    plate = forms.CharField(
        validators=[
            RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}")],
            max_length=8)



        
    