
from rest_framework import serializers
from parking.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'plate', 'timeOut', 'pay']