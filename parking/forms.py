from django.core.exceptions import ValidationError
from django import forms
from re import search


class FormReservation(forms.Form):
    plate = forms.CharField()

    def clean_reservation(self):
        data = self.cleaned_data['plate']

        if not search("^[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}",self.plate):
            raise ValidationError("Invalidate plate")
        
        return data 



        
    