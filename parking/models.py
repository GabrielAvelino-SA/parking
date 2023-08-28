from django.db import models

class Reservation(models.Model):
    models.AutoField(primary_key=True)
    timeOut = models.TimeField()
    #plate = 
    #pay =