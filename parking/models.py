from django.db import models
from django.core.validators import RegexValidator

class Reservation(models.Model):
    plate = models.CharField(
        validators=[RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}", message="Wrong Format")],
        max_length=8,
        unique=True)
    time = models.TimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, blank=False)
    left = models.BooleanField(default=False, blank=False)

    def create(self, **validated_data):
         return Reservation.objects.create(**validated_data)
    
    def get_values(self):
        return [(field, field.value_to_string(self)) for field in Reservation._meta.fields]
    
    def __str__(self):
        return self.plate
    
class Historico(models.Model):
    id_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, to_field='id')
    date = models.DateField(auto_now=True)
    time = models.DurationField()

    def create(self, **validated_data):
         return Historico.objects.create(**validated_data)

    def __str__(self) :
        return self.id_plate
        