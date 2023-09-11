from rest_framework import serializers
from django.core.validators import RegexValidator
from parking.models import Reservation

class ReservationSerializer(serializers.Serializer):
    
    id =  serializers.IntegerField(read_only=True)
    plate = serializers.CharField(
        max_length=8,
        read_only = True, 
        validators=[
            RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}", 
            message="Wrong Format")]
        )
    time = serializers.TimeField(read_only=True)
    paid = serializers.BooleanField(default=False)
    left = serializers.BooleanField(default=False)

    #Methods ReservetionSerializer
    def create(self,validated_data):
        '''
        Create and return a new Reservation given the validate  
        '''

        return Reservation.objects.create(**validated_data)
    
    def update(self,instance,validate_data):
        '''
        update and return and existent reservation
        '''
        instance.paid = validate_data.get('paid', instance.paid)
        instance.left = validate_data.get('left', instance.left)
        instance.save()
        return instance

class TimeSerializer(serializers.Serializer):
    time = serializers.TimeField(read_only=True)
    paid = serializers.BooleanField(default=False)
    left = serializers.BooleanField(default=False)

