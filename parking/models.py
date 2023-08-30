from django.db import models

class Reservation(models.Model):
    plate = models.CharField(max_length=8)
    timeOut = models.TimeField("Time started")
    pay = models.BooleanField(default=False)

    def __str__(self):
        return self.plate