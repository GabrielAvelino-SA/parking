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
    
    def __str__(self):
        return self.plate
    
    class Historico(models.model):
        id_plate = ""#foreing =key
        check_in = ""#check in
        check_out = ""#check out
        