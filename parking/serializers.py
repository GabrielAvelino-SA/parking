
from rest_framework import serializers
from parking.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        id =  serializers.IntegerField(read_only=True)
        plate = serializers.CharField(max_length=8)
        timeOut = serializers.TimeField("Time started")
        pay = serializers.BooleanField(default=False)

        model = Reservation
        fields = ['id', 'plate', 'timeOut', 'pay']
        
        def create(self,validated_data):
            '''
            validação dos dados
            '''
            return Reservation.objects.create(validated_data)
        
        def update(self,instance,validate_data):
            instance.plate = validate_data.get('plate',instance.plate)
            instance.timeOut = validate_data.get('timeout',instance.timeOut)
            instance.pay = validate_data.get ('pay', instance.pay)
            instance.save()
            return instance
