from django.db import models

class Reservation(models.Model):
    plate = models.CharField(max_length=8)
    time = models.TimeField(auto_now_add=True, auto_now=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.plate