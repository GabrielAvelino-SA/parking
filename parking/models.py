from collections.abc import Collection
from typing import Any
from django.db import models
from django.core.validators import RegexValidator


class Reservation(models.Model):
    plate = models.CharField(
        validators=[
            RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}", 
            message="The Format plate is no Valid")],
            max_length=8,
            unique=True)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, blank=False)
    left = models.BooleanField(default=False, blank=False)

    # def clean(self);
    #     cleaned_data =

    def create(self, **validated_data):
         return Reservation.objects.create(**validated_data)
    
    def __str__(self):
        return self.plate
    
class Historico(models.Model):
    id_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, to_field='id')
    checkIn = models.DateTimeField()
    checkOut = models.DateTimeField(null=True, blank=True)

    def create(self, **validated_data):
         return Historico.objects.create(**validated_data)

    def __str__(self) :
        return self.id_reservation.plate
    
    def get_deltaTime(self):
        try: 
            time = self.checkOut - self.checkIn
            return time
        except:
           return None