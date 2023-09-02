from rest_framework import serializers
from parking.models import Reservation
import datatime

class ReservationSerializer(serializers.Serializer):
    id =  serializers.IntegerField(read_only=True)
    plate = serializers.CharField(max_length=8, write_only=True)
    timeOut = serializers.TimeField("Time started")
    pay = serializers.BooleanField(default=False)

    #Methods of Reservetion Serializer
    def create(self,validated_data):
        '''
        Create and return a new Reservation given the validate  
        '''
        return Reservation.objects.create(validated_data)
    
    def update(self,instance,validate_data):
        '''
        update and return and existent reservation
        '''
        instance.plate = validate_data.get('plate',instance.plate)
        instance.timeOut = validate_data.get('timeout',instance.timeOut)
        instance.pay = validate_data.get ('pay', instance.pay)
        instance.save()
        return instance
