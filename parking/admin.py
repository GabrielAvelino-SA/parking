from django.contrib import admin
from parking.models import Reservation, Historico

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Historico)
