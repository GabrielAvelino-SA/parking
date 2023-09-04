from rest_framework import serializers
from parking.models import Reservation

class ReservationSerializer(serializers.Serializer):
    id =  serializers.IntegerField(read_only=True)
    plate = serializers.CharField(max_length=8)
    time = serializers.TimeField(required = False)
    paid = serializers.BooleanField(default=False)

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
        instance.paid = validate_data.get ('paid', instance.paid)
        instance.save()
        return instance
