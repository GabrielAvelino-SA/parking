from django import forms
from parking.models import Reservation
from django.core.validators import RegexValidator
from re import search


class FormReservation(forms.ModelForm):
    plate = forms.CharField(
        validators=[
            RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}",
            message = "Plate should be it a combination valid")
            ],
        max_length=8
        )
    paid = forms.BooleanField(default = False)
    left = forms.BooleanField(default = False)
    
    def clean(self):
        cleaned_data = super(FormReservation, self).clean()
        # additional cleaning here
        return cleaned_data

    class Meta:
        model = Reservation
        fields = "__all__"

    # def clean_plate(self):
    #     plate = self.cleaned_data['plate']
    #     if 



        
    